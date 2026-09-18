from django.test import TestCase, Client, RequestFactory, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.models import UserProfile
from accounts.forms import generate_math_challenge
from ai_prompts.models import PromptCategory, AIPrompt, PromptAssistanceRequest
import decimal


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ClientAccountAndPromptsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        
        # Test Category
        self.category = PromptCategory.objects.create(
            name="Google Apps Script & Sheets",
            slug="google-apps-script-sheets"
        )
        
        # Test Prompt
        self.prompt = AIPrompt.objects.create(
            category=self.category,
            title="Complete Car Marketplace Google Apps Script",
            slug="complete-car-marketplace",
            tagline="Car marketplace web app",
            overview="Build complete car marketplace with Google Sheets",
            master_prompt="You are an expert engineer. Build a car marketplace...",
            is_free=False,
            price_kes=decimal.Decimal("1500.00"),
            price_usd=decimal.Decimal("12.00"),
            assistance_price_kes=decimal.Decimal("2500.00"),
            assistance_price_usd=decimal.Decimal("20.00"),
            is_published=True
        )

    def test_math_challenge_generation(self):
        """Test that dynamic math challenge generates question and stores answer in session."""
        request = self.factory.get('/account/register/')
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()

        question, answer = generate_math_challenge(request)
        self.assertTrue('+' in question or '-' in question)
        self.assertEqual(int(request.session.get('utc_math_answer')), answer)

    def test_registration_with_valid_phone_and_math(self):
        """Test client registration with valid international phone number starting with +."""
        session = self.client.session
        session['utc_math_answer'] = '15'
        session.save()

        data = {
            'first_name': 'Test',
            'last_name': 'Client',
            'username': 'testclient',
            'email': 'testclient@example.com',
            'phone_number': '+254715479955',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
            'math_answer': '15',
            'agree_terms': True,
        }
        res = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(res.status_code, 302)
        
        # Verify user and profile
        user = User.objects.get(username='testclient')
        self.assertEqual(user.email, 'testclient@example.com')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.phone_number, '+254715479955')
        self.assertFalse(user.profile.is_email_verified)
        self.assertTrue(len(user.profile.email_verification_token) > 0)

    def test_registration_rejects_invalid_phone_without_country_code(self):
        """Test that registration rejects phone numbers not starting with '+' and country code."""
        session = self.client.session
        session['utc_math_answer'] = '10'
        session.save()

        data = {
            'first_name': 'Bad',
            'last_name': 'Phone',
            'username': 'badphoneuser',
            'email': 'badphone@example.com',
            'phone_number': '0715479955',  # Missing +country code
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
            'math_answer': '10',
            'agree_terms': True,
        }
        res = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(User.objects.filter(username='badphoneuser').exists())

    def test_dual_login_with_username_and_email(self):
        """Test that clients can authenticate with either username OR email with math challenge."""
        user = User.objects.create_user(
            username='johndoe',
            email='john.doe@example.com',
            password='MyPassword456!'
        )
        UserProfile.objects.create(user=user, phone_number='+254700112233')

        session = self.client.session
        session['utc_math_answer'] = '20'
        session.save()

        # 1. Login with username
        res_username = self.client.post(reverse('accounts:login'), {
            'login_identifier': 'johndoe',
            'password': 'MyPassword456!',
            'math_answer': '20',
        })
        self.assertEqual(res_username.status_code, 302)
        self.client.logout()

        session = self.client.session
        session['utc_math_answer'] = '20'
        session.save()

        # 2. Login with email
        res_email = self.client.post(reverse('accounts:login'), {
            'login_identifier': 'john.doe@example.com',
            'password': 'MyPassword456!',
            'math_answer': '20',
        })
        self.assertEqual(res_email.status_code, 302)

    def test_prompts_list_and_detail_views(self):
        """Test AI Prompts catalog and detail page responses."""
        res_list = self.client.get(reverse('ai_prompts:list'))
        self.assertEqual(res_list.status_code, 200)
        self.assertContains(res_list, "Complete Car Marketplace")
        self.assertContains(res_list, "5797853")

        res_detail = self.client.get(reverse('ai_prompts:detail', kwargs={'slug': self.prompt.slug}))
        self.assertEqual(res_detail.status_code, 200)
        self.assertContains(res_detail, "5797853")
        # Since prompt is paid and not purchased yet, it shows payment verification
        self.assertContains(res_detail, "Unlock Prompt")

    def test_copy_prompt_api(self):
        """Test that copy API requires access on paid prompts and increments count on free/authorized prompts."""
        # Unpaid attempt should return 403
        res_locked = self.client.post(reverse('ai_prompts:copy_api', kwargs={'slug': self.prompt.slug}))
        self.assertEqual(res_locked.status_code, 403)

        # On free prompt, should succeed and increment count
        self.prompt.is_free = True
        self.prompt.save()
        initial_copies = self.prompt.copy_count
        res = self.client.post(reverse('ai_prompts:copy_api', kwargs={'slug': self.prompt.slug}))
        self.assertEqual(res.status_code, 200)
        self.prompt.refresh_from_db()
        self.assertEqual(self.prompt.copy_count, initial_copies + 1)

    def test_download_prompt(self):
        """Test that download requires access on paid prompts and allows download on free/authorized prompts."""
        # Unpaid attempt redirects to detail
        res_locked = self.client.get(reverse('ai_prompts:download', kwargs={'slug': self.prompt.slug}))
        self.assertEqual(res_locked.status_code, 302)

        # On free prompt, downloading markdown succeeds
        self.prompt.is_free = True
        self.prompt.save()
        res = self.client.get(reverse('ai_prompts:download', kwargs={'slug': self.prompt.slug}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'text/markdown; charset=utf-8')
        self.assertIn('attachment', res['Content-Disposition'])
