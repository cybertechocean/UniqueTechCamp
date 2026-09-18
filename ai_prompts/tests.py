from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PromptCategory, AIPrompt, PromptPurchase


class AIPromptAccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = PromptCategory.objects.create(name="Web Apps", slug="web-apps")

        self.free_prompt = AIPrompt.objects.create(
            category=self.category,
            title="Free Starter Prompt",
            slug="free-starter-prompt",
            tagline="Starter coding prompt",
            overview="Build a starter app",
            master_prompt="PROMPT: Build a simple web app.",
            is_free=True,
            price_kes=0.00,
            is_published=True
        )

        self.paid_prompt = AIPrompt.objects.create(
            category=self.category,
            title="Paid Retail POS Engine",
            slug="paid-retail-pos-engine",
            tagline="Full-stack POS and M-Pesa",
            overview="Build a retail POS app",
            master_prompt="SECRET MASTER PROMPT: Full enterprise POS source code.",
            is_free=False,
            price_kes=2500.00,
            price_usd=25.00,
            is_published=True
        )

        # Create user WITHOUT profile (to test User has no profile bug)
        self.user_no_profile = User.objects.create_user(
            username="testarchitect",
            email="architect@example.com",
            password="SecurePassword123!"
        )

    def test_prompt_detail_view_user_has_no_profile_bug_fixed(self):
        """
        Verify that a logged-in user without an existing UserProfile does not
        trigger RelatedObjectDoesNotExist exception on prompt detail page.
        """
        self.client.login(username="testarchitect", password="SecurePassword123!")
        res = self.client.get(reverse('ai_prompts:detail', kwargs={'slug': self.paid_prompt.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.context['has_access'])
        # Verify secret master prompt is NOT in the HTML response for unpaid users
        self.assertNotIn("SECRET MASTER PROMPT: Full enterprise POS source code.", res.content.decode())

    def test_free_prompt_accessible_to_all(self):
        """Free prompts must be viewable, copyable, and downloadable by everyone."""
        res = self.client.get(reverse('ai_prompts:detail', kwargs={'slug': self.free_prompt.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context['has_access'])
        self.assertIn("PROMPT: Build a simple web app.", res.content.decode())

        # Test copy API
        copy_res = self.client.post(reverse('ai_prompts:copy_api', kwargs={'slug': self.free_prompt.slug}))
        self.assertEqual(copy_res.status_code, 200)
        self.assertTrue(copy_res.json()['success'])

        # Test download
        dl_res = self.client.get(reverse('ai_prompts:download', kwargs={'slug': self.free_prompt.slug}))
        self.assertEqual(dl_res.status_code, 200)
        self.assertIn("PROMPT: Build a simple web app.", dl_res.content.decode())

    def test_paid_prompt_locked_until_verified(self):
        """Paid prompts must reject copy API (403) and download when not verified."""
        # Test copy without access
        copy_res = self.client.post(reverse('ai_prompts:copy_api', kwargs={'slug': self.paid_prompt.slug}))
        self.assertEqual(copy_res.status_code, 403)
        self.assertFalse(copy_res.json()['success'])

        # Test download without access
        dl_res = self.client.get(reverse('ai_prompts:download', kwargs={'slug': self.paid_prompt.slug}))
        self.assertEqual(dl_res.status_code, 302)  # redirects to prompt page

    def test_payment_submission_and_admin_unlock(self):
        """
        Client submits payment reference, status starts as pending,
        and once verified, full prompt becomes unlocked.
        """
        self.client.login(username="testarchitect", password="SecurePassword123!")

        post_data = {
            'client_name': 'Lawi Otieno',
            'client_email': 'architect@example.com',
            'client_phone': '+254715479955',
            'payment_method': 'mpesa_till',
            'transaction_code': 'UII9O6P15V',
            'payment_message': 'Confirmed. KES 2500 sent to Till 5797853',
        }
        res = self.client.post(
            reverse('ai_prompts:payment_submit', kwargs={'slug': self.paid_prompt.slug}),
            data=post_data
        )
        self.assertEqual(res.status_code, 302)

        # Check DB record
        purchase = PromptPurchase.objects.get(prompt=self.paid_prompt, client_email='architect@example.com')
        self.assertEqual(purchase.transaction_code, 'UII9O6P15V')
        self.assertFalse(purchase.is_verified)
        self.assertEqual(purchase.status, 'pending')

        # Check detail page shows pending
        detail_res = self.client.get(reverse('ai_prompts:detail', kwargs={'slug': self.paid_prompt.slug}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertFalse(detail_res.context['has_access'])
        self.assertIsNotNone(detail_res.context['pending_purchase'])

        # Admin approves in Django Admin
        purchase.is_verified = True
        purchase.save()

        # Check prompt is now unlocked
        unlocked_res = self.client.get(reverse('ai_prompts:detail', kwargs={'slug': self.paid_prompt.slug}))
        self.assertEqual(unlocked_res.status_code, 200)
        self.assertTrue(unlocked_res.context['has_access'])
        self.assertIn("SECRET MASTER PROMPT: Full enterprise POS source code.", unlocked_res.content.decode())

        # Copy & Download now succeed
        copy_res = self.client.post(reverse('ai_prompts:copy_api', kwargs={'slug': self.paid_prompt.slug}))
        self.assertEqual(copy_res.status_code, 200)
        self.assertTrue(copy_res.json()['success'])

        dl_res = self.client.get(reverse('ai_prompts:download', kwargs={'slug': self.paid_prompt.slug}))
        self.assertEqual(dl_res.status_code, 200)
        self.assertIn("SECRET MASTER PROMPT: Full enterprise POS source code.", dl_res.content.decode())
