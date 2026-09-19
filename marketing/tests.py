from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from marketing.models import BulkCampaign, CampaignRecipient, EmailLog, EmailSuppressionList
from marketing.dispatcher import dispatch_next_campaign_recipient, send_single_campaign_email
from marketing.validator import (
    clean_and_normalize_email,
    is_valid_syntax,
    is_disposable,
    is_dangerous_spam_trap,
    is_hard_bounce_error,
    verify_email_deliverability
)

User = get_user_model()

@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
)
class BulkMarketingEngineTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff_tester',
            password='secretpassword123',
            is_staff=True,
        )
        self.client = Client()
        self.client.login(username='staff_tester', password='secretpassword123')

        self.campaign = BulkCampaign.objects.create(
            title='Test Tech Broadcast',
            sender_name='UTC Marketing',
            sender_email='info@uniquetechcamp.org',
            sender_choice='email1',
            email_format='branded',
            delay_seconds=0.0,
            total_recipients=2,
            status='draft'
        )

        self.r1 = CampaignRecipient.objects.create(
            campaign=self.campaign,
            name='Alice Client',
            email='alice@example.com',
            subject='Website Modernization Proposal',
            personalized_message='Hello Alice, we would love to build your platform.'
        )
        self.r2 = CampaignRecipient.objects.create(
            campaign=self.campaign,
            name='Bob Business',
            email='bob@example.com',
            subject='AI Automation Services',
            personalized_message='Hello Bob, enhance your workflows with AI.'
        )

    def test_step_by_step_dispatch(self):
        """Verify that dispatch_next_campaign_recipient processes one recipient at a time."""
        # Step 1
        res1 = dispatch_next_campaign_recipient(self.campaign)
        self.campaign.refresh_from_db()
        self.r1.refresh_from_db()

        self.assertFalse(res1['completed'])
        self.assertEqual(res1['recipient_email'], 'alice@example.com')
        self.assertEqual(self.r1.status, 'sent')
        self.assertEqual(self.campaign.sent_count, 1)
        self.assertEqual(self.campaign.status, 'sending')

        # Step 2
        res2 = dispatch_next_campaign_recipient(self.campaign)
        self.campaign.refresh_from_db()
        self.r2.refresh_from_db()

        self.assertTrue(res2['completed'])
        self.assertEqual(res2['recipient_email'], 'bob@example.com')
        self.assertEqual(self.r2.status, 'sent')
        self.assertEqual(self.campaign.sent_count, 2)
        self.assertEqual(self.campaign.status, 'completed')

    def test_campaign_reset_status_view(self):
        """Verify that reset_status unlocks a campaign stuck in 'sending'."""
        self.campaign.status = 'sending'
        self.campaign.save()

        url = reverse('marketing:reset_status', kwargs={'pk': self.campaign.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.status, 'draft')

    def test_dispatch_step_api_view(self):
        """Verify the JSON step dispatch API endpoint."""
        url = reverse('marketing:campaign_dispatch_step_api', kwargs={'pk': self.campaign.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['recipient_email'], 'alice@example.com')
        self.assertEqual(data['sent_count'], 1)
        self.assertEqual(data['remaining_count'], 1)

    def test_validator_typo_correction(self):
        """Verify automatic domain typo correction for scraped emails."""
        cleaned, fixed = clean_and_normalize_email("  <narokcounty@gamil.com>  ")
        self.assertEqual(cleaned, "narokcounty@gmail.com")
        self.assertTrue(fixed)

        cleaned2, fixed2 = clean_and_normalize_email("test@yaho.com,")
        self.assertEqual(cleaned2, "test@yahoo.com")
        self.assertTrue(fixed2)

    def test_validator_disposable_and_spam_trap(self):
        """Verify disposable emails and spam trap addresses are detected."""
        self.assertTrue(is_disposable("user@mailinator.com"))
        self.assertTrue(is_disposable("fake@tempmail.com"))
        self.assertFalse(is_disposable("contact@uniquetechcamp.org"))

        self.assertTrue(is_dangerous_spam_trap("abuse@example.com"))
        self.assertTrue(is_dangerous_spam_trap("postmaster@domain.com"))
        self.assertTrue(is_dangerous_spam_trap("spam@domain.com"))
        self.assertFalse(is_dangerous_spam_trap("sales@domain.com"))

    def test_hard_bounce_detection(self):
        """Verify hard bounce 550 strings are accurately detected."""
        err1 = "550-5.1.1 The email account that you tried to reach does not exist. https://support.google.com/mail/?p=NoSuchUser"
        self.assertTrue(is_hard_bounce_error(err1))

        err2 = "550 User unknown"
        self.assertTrue(is_hard_bounce_error(err2))

        err3 = "Connection refused (port 465)"
        self.assertFalse(is_hard_bounce_error(err3))

    def test_suppression_list_blocks_send(self):
        """Verify that an email in EmailSuppressionList is blocked from sending."""
        EmailSuppressionList.objects.create(
            email='bounced_user@example.com',
            reason='hard_bounce',
            detail='550 NoSuchUser'
        )

        bad_recipient = CampaignRecipient.objects.create(
            campaign=self.campaign,
            name='Bounced Guy',
            email='bounced_user@example.com',
            subject='Hello',
            personalized_message='Test message'
        )

        success, err = send_single_campaign_email(bad_recipient)
        self.assertFalse(success)
        bad_recipient.refresh_from_db()
        self.assertEqual(bad_recipient.status, 'failed')
        self.assertIn('Reputation Shield', bad_recipient.error_message)

    def test_prune_invalid_view(self):
        """Verify pruning removes invalid/suppressed contacts from campaign queue."""
        CampaignRecipient.objects.create(
            campaign=self.campaign,
            name='Dead Guy',
            email='dead@fake_domain_xyz_12345.com',
            subject='Hello',
            personalized_message='Test message',
            verification_status='invalid',
            is_deliverable=False,
            status='pending'
        )
        self.campaign.total_recipients = self.campaign.recipients.count()
        self.campaign.save()

        initial_count = self.campaign.recipients.count()

        url = reverse('marketing:prune_invalid', kwargs={'pk': self.campaign.id})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)

        self.campaign.refresh_from_db()
        self.assertLess(self.campaign.recipients.count(), initial_count)
        self.assertFalse(self.campaign.recipients.filter(email='dead@fake_domain_xyz_12345.com').exists())

    def test_bulk_recipient_mark_bounced_and_suppression(self):
        """Verify that checking and marking contacts as bounced updates status and permanently suppresses them."""
        url = reverse('marketing:bulk_recipients', kwargs={'pk': self.campaign.id})
        response = self.client.post(
            url,
            data={'action': 'mark_bounced', 'recipient_ids': [self.r1.id]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        self.r1.refresh_from_db()
        self.assertEqual(self.r1.status, 'failed')
        self.assertEqual(self.r1.verification_status, 'suppressed')
        self.assertFalse(self.r1.is_deliverable)
        self.assertIn('550', self.r1.error_message)

        # Confirm global suppression list entry was created
        suppressed_entry = EmailSuppressionList.objects.filter(email='alice@example.com').first()
        self.assertIsNotNone(suppressed_entry)
        self.assertEqual(suppressed_entry.reason, 'hard_bounce')

    def test_bulk_recipient_delete(self):
        """Verify that bulk delete removes selected recipients from queue and recalculates counts."""
        url = reverse('marketing:bulk_recipients', kwargs={'pk': self.campaign.id})
        response = self.client.post(
            url,
            data={'action': 'delete', 'recipient_ids': [self.r2.id]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        self.assertFalse(CampaignRecipient.objects.filter(id=self.r2.id).exists())
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.total_recipients, 1)

    def test_scrape_anomaly_detection(self):
        """Verify that corrupted emails scraped from web/PDFs are detected and blocked."""
        from marketing.validator import detect_scrape_anomaly

        corrupt1, r1 = detect_scrape_anomaly("contact@domain.con")
        self.assertTrue(corrupt1)
        self.assertIn(".con", r1)

        corrupt2, r2 = detect_scrape_anomaly("info@gmail.comphone")
        self.assertTrue(corrupt2)
        self.assertIn("Scraped text glued", r2)

        corrupt3, r3 = detect_scrape_anomaly("a@gmail.com")
        self.assertTrue(corrupt3)
        self.assertIn("truncated username", r3)

        ok, _ = detect_scrape_anomaly("valid.user@gmail.com")
        self.assertFalse(ok)
