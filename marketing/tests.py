from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from marketing.models import BulkCampaign, CampaignRecipient, EmailLog
from marketing.dispatcher import dispatch_next_campaign_recipient

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
