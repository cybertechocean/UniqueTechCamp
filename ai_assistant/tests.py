import json
import datetime
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from appointments.models import Appointment
from .models import LeadCapture, ChatSession, ChatMessage
from .availability import get_available_slots_for_date, find_next_available_dates
from .gemini_engine import generate_conversational_response, FREE_TIER_MODELS_CASCADE


class AiAssistantTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        # Ensure tomorrow is not Saturday (weekday 5) since Saturday is closed
        while self.tomorrow.weekday() == 5:
            self.tomorrow += datetime.timedelta(days=1)

    def test_session_init_creates_session_and_welcome(self):
        """Tests that session initialization generates a UUID and welcoming intro message."""
        url = reverse('ai_assistant:api_init')
        res = self.client.post(url, data=json.dumps({}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['session_id'])
        self.assertFalse(data['has_lead'])
        self.assertGreaterEqual(len(data['messages']), 1)
        self.assertEqual(data['messages'][0]['sender'], 'assistant')

    def test_lead_capture_validation_and_storage(self):
        """Tests that LeadCapture validates email syntax and creates record linked to session."""
        init_res = self.client.post(reverse('ai_assistant:api_init'), data=json.dumps({}), content_type='application/json')
        session_id = init_res.json()['session_id']

        # Missing phone should fail
        res_fail = self.client.post(
            reverse('ai_assistant:api_capture_lead'),
            data=json.dumps({
                'session_id': session_id,
                'full_name': 'John Doe',
                'email': 'invalid-email',
                'phone': ''
            }),
            content_type='application/json'
        )
        self.assertEqual(res_fail.status_code, 400)

        # Valid payload
        res_ok = self.client.post(
            reverse('ai_assistant:api_capture_lead'),
            data=json.dumps({
                'session_id': session_id,
                'full_name': 'Dr. Angela Mwangi',
                'email': 'angela.mwangi@example.com',
                'phone': '+254712345678',
                'industry': 'Healthcare & Private Clinics',
                'business_bottleneck': 'Need automated patient queues and WhatsApp reminders'
            }),
            content_type='application/json'
        )
        self.assertEqual(res_ok.status_code, 200)
        data = res_ok.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['has_lead'])

        # Verify database record
        lead = LeadCapture.objects.get(email='angela.mwangi@example.com')
        self.assertEqual(lead.full_name, 'Dr. Angela Mwangi')
        self.assertEqual(lead.phone, '+254712345678')
        self.assertTrue(lead.admin_alert_sent)

        # Verify session link
        session = ChatSession.objects.get(session_id=session_id)
        self.assertEqual(session.lead, lead)
        self.assertEqual(session.status, 'lead_captured')

    def test_pending_query_preservation_and_fulfillment(self):
        """Tests that an inquiry asked before lead registration is preserved and answered immediately upon lead capture."""
        init_res = self.client.post(reverse('ai_assistant:api_init'), data=json.dumps({}), content_type='application/json')
        session_id = init_res.json()['session_id']

        # User asks question before giving details
        q_res = self.client.post(
            reverse('ai_assistant:api_message'),
            data=json.dumps({
                'session_id': session_id,
                'message': 'Do you build clinic management systems?'
            }),
            content_type='application/json'
        )
        self.assertEqual(q_res.status_code, 200)
        self.assertEqual(q_res.json()['action_type'], 'lead_form')

        session = ChatSession.objects.get(session_id=session_id)
        self.assertEqual(session.pending_query, 'Do you build clinic management systems?')

        # User now submits details -> pending query should be answered
        cap_res = self.client.post(
            reverse('ai_assistant:api_capture_lead'),
            data=json.dumps({
                'session_id': session_id,
                'full_name': 'Dr. Brian Kamau',
                'email': 'brian.kamau@example.com',
                'phone': '+254722112233'
            }),
            content_type='application/json'
        )
        self.assertEqual(cap_res.status_code, 200)
        self.assertIn('Do you build clinic management systems?', cap_res.json()['reply'])

    def test_availability_engine(self):
        """Tests Saturday closure check and Sunday/weekday slot availability verification."""
        # Test a Saturday
        saturday = timezone.now().date()
        while saturday.weekday() != 5:
            saturday += datetime.timedelta(days=1)

        sat_slots = get_available_slots_for_date(saturday)
        self.assertFalse(sat_slots['is_operating_day'])

        # Test Sunday (now an operating day!)
        sunday = timezone.now().date()
        while sunday.weekday() != 6:
            sunday += datetime.timedelta(days=1)

        sun_slots = get_available_slots_for_date(sunday)
        self.assertTrue(sun_slots['is_operating_day'])
        self.assertGreaterEqual(len(sun_slots['slots']), 6)

        # Test valid business date
        biz_date = self.tomorrow
        biz_slots = get_available_slots_for_date(biz_date)
        self.assertTrue(biz_slots['is_operating_day'])
        self.assertGreaterEqual(len(biz_slots['slots']), 6)

        # Occupy a slot and verify it reflects as not available
        Appointment.objects.create(
            full_name="Existing Client",
            email="existing@example.com",
            phone="+254700000000",
            preferred_date=biz_date,
            preferred_time_slot='10:30 - 11:30',
            status='confirmed',
            source='web_form'
        )
        updated_slots = get_available_slots_for_date(biz_date)
        occupied_slot = next(s for s in updated_slots['slots'] if s['slot_key'] == '10:30 - 11:30')
        self.assertFalse(occupied_slot['is_available'])

    def test_direct_consultation_booking_via_ai(self):
        """Tests booking a consultation directly through the AI assistant and verifying source attribution."""
        init_res = self.client.post(reverse('ai_assistant:api_init'), data=json.dumps({}), content_type='application/json')
        session_id = init_res.json()['session_id']

        # Capture lead
        self.client.post(
            reverse('ai_assistant:api_capture_lead'),
            data=json.dumps({
                'session_id': session_id,
                'full_name': 'Sarah Njoroge',
                'email': 'sarah.njoroge@example.com',
                'phone': '+254799887766',
                'industry': 'Retail E-Commerce'
            }),
            content_type='application/json'
        )

        # Book consultation
        book_res = self.client.post(
            reverse('ai_assistant:api_book'),
            data=json.dumps({
                'session_id': session_id,
                'date': self.tomorrow.strftime('%Y-%m-%d'),
                'slot_key': '14:00 - 15:00',
                'meeting_type': 'google_meet',
                'description': 'E-Commerce storefront with M-Pesa integration'
            }),
            content_type='application/json'
        )
        self.assertEqual(book_res.status_code, 200)
        data = book_res.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['action_type'], 'booking_card')

        # Verify created appointment
        ref = data['metadata']['reference']
        apt = Appointment.objects.get(booking_reference=ref)
        self.assertEqual(apt.full_name, 'Sarah Njoroge')
        self.assertEqual(apt.email, 'sarah.njoroge@example.com')
        self.assertEqual(apt.source, 'ai_assistant')  # Clear attribution!

    def test_multi_model_cascade_fallback_resilience(self):
        """Tests that when an active Gemini model raises a quota error, it cascades silently to the next model."""
        import urllib.error
        
        # Simulate HTTP 429 on first model, success on second model
        def mock_call_gemini(model, api_key, system_prompt, chat_history, timeout=15):
            if model == FREE_TIER_MODELS_CASCADE[0]:
                raise urllib.error.HTTPError(
                    url="https://api.test", code=429, msg="Too Many Requests", hdrs={}, fp=None
                )
            return "Cascaded response successfully generated by fallback model."

        with patch('ai_assistant.gemini_engine.call_gemini_api', side_effect=mock_call_gemini):
            with patch('django.conf.settings.GEMINI_API_KEY', 'test-fake-key'):
                result = generate_conversational_response([], "Tell me about your services")
                self.assertTrue(result['is_fallback'])
                self.assertEqual(result['model_used'], FREE_TIER_MODELS_CASCADE[1])
                self.assertIn("Cascaded response successfully generated", result['text'])

    def test_dedicated_fullpage_route_renders(self):
        """Tests that the dedicated /ai-assistant/ route renders with 200 OK and expected elements."""
        res = self.client.get(reverse('ai_assistant:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "AI Solutions Architect")
        self.assertContains(res, "AI Architecture Desk")
