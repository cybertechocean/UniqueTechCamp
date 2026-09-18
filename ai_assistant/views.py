import json
import re
import datetime
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.conf import settings

from appointments.models import Appointment
from appointments.emails import send_appointment_emails
from services.models import ServiceCategory, Service
from .models import ChatSession, ChatMessage, LeadCapture
from .gemini_engine import generate_conversational_response
from .availability import get_available_slots_for_date, find_next_available_dates
from .emails import send_lead_transcript_email, send_lead_admin_alert_email

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class AiAssistantPageView(View):
    """
    Dedicated full-screen conversational workspace for UniqueTechCamp.
    Provides category exploration chips, guarantees, and interactive project scoping.
    """
    def get(self, request):
        categories = ServiceCategory.objects.filter(is_active=True).order_by('order')[:9]
        upcoming_dates = find_next_available_dates(3)
        context = {
            'categories': categories,
            'upcoming_dates': upcoming_dates,
            'page_title': "AI Solutions Architect & Project Consultation | UniqueTechCamp",
            'meta_description': "Consult with UniqueTechCamp's 24/7 AI Solutions Architect to scope custom web systems, WhatsApp AI bots, clinic management platforms, and schedule discovery consultations.",
        }
        return render(request, 'ai_assistant/assistant_page.html', context)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ChatInitApiView(View):
    """
    Initializes or resumes a chat session. Returns historical messages and lead status.
    """
    def post(self, request):
        try:
            body = json.loads(request.body or '{}')
        except Exception:
            body = {}

        session_id_str = body.get('session_id') or request.session.get('ai_chat_session_id')
        session = None

        # Determine authenticated user
        user = request.user if request.user.is_authenticated else None

        if session_id_str:
            try:
                session = ChatSession.objects.filter(session_id=session_id_str, is_active=True).first()
            except Exception:
                session = None

        # If user is authenticated and no session found by ID, pick their most recent active session
        if user and not session:
            session = ChatSession.objects.filter(user=user, is_active=True).order_by('-created_at').first()

        if not session:
            session = ChatSession.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:400],
            )
            request.session['ai_chat_session_id'] = str(session.session_id)

            # Auto-link lead if client is logged in
            if user:
                phone = user.profile.phone if hasattr(user, 'profile') and user.profile.phone else ''
                lead, _ = LeadCapture.objects.get_or_create(
                    email=user.email,
                    defaults={
                        'full_name': user.get_full_name() or user.username,
                        'phone': phone,
                    }
                )
                session.lead = lead
                session.status = 'lead_captured'
                session.save(update_fields=['lead', 'status'])

            # Single short welcome message as requested (no immediate lead form)
            initial_welcome = (
                "Welcome to UniqueTechCamp! I am your 24/7 AI Solutions Architect. "
                "We develop/engineer high-converting web applications, 24/7 WhatsApp/Email qualification bots, "
                "clinic systems, and e-commerce platforms."
            )
            ChatMessage.objects.create(
                session=session,
                sender='assistant',
                message=initial_welcome,
                model_used='system-desk',
                action_type='normal'
            )
        elif user and not session.lead:
            # Associate logged-in user with existing anonymous session
            session.user = user
            phone = user.profile.phone if hasattr(user, 'profile') and user.profile.phone else ''
            lead, _ = LeadCapture.objects.get_or_create(
                email=user.email,
                defaults={
                    'full_name': user.get_full_name() or user.username,
                    'phone': phone,
                }
            )
            session.lead = lead
            session.status = 'lead_captured'
            session.save(update_fields=['user', 'lead', 'status'])

        # Serialize messages
        messages_data = []
        for msg in session.messages.order_by('created_at'):
            messages_data.append({
                'id': msg.id,
                'sender': msg.sender,
                'message': msg.message,
                'model_used': msg.model_used,
                'action_type': msg.action_type,
                'metadata': msg.metadata,
                'created_at': msg.created_at.isoformat(),
            })

        return JsonResponse({
            'success': True,
            'session_id': str(session.session_id),
            'has_lead': bool(session.lead),
            'lead_name': session.lead.full_name if session.lead else '',
            'status': session.status,
            'messages': messages_data,
        })


class SendMessageApiView(View):
    """
    Receives user query. If no lead is on file, preserves intent in pending_query and requests lead info.
    If lead is on file, fulfills query via Gemini cascade or triggers appointment slot picker.
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

        session_id = data.get('session_id')
        user_message = (data.get('message') or '').strip()

        if not session_id or not user_message:
            return JsonResponse({'success': False, 'error': 'session_id and message are required'}, status=400)

        session = get_object_or_404(ChatSession, session_id=session_id)

        # 1. Record User's Message
        ChatMessage.objects.create(
            session=session,
            sender='user',
            message=user_message,
        )

        # 2. Check if user is authenticated and auto-link lead if missing
        if request.user.is_authenticated and not session.lead:
            session.user = request.user
            phone = request.user.profile.phone if hasattr(request.user, 'profile') and request.user.profile.phone else ''
            lead, _ = LeadCapture.objects.get_or_create(
                email=request.user.email,
                defaults={
                    'full_name': request.user.get_full_name() or request.user.username,
                    'phone': phone,
                }
            )
            session.lead = lead
            session.status = 'lead_captured'
            session.save(update_fields=['user', 'lead', 'status'])

        # 3. Check if Lead Info is Secured
        if not session.lead:
            # Preserve user's pending query so we answer it the moment contact details are submitted
            session.pending_query = user_message
            session.save(update_fields=['pending_query'])

            lead_request_msg = (
                "Thank you for reaching out! To tailor our technical recommendations specifically for your project, "
                "deliver your full session transcript, and connect you directly with our senior engineers, please "
                "share your contact details below:"
            )
            bot_msg = ChatMessage.objects.create(
                session=session,
                sender='assistant',
                message=lead_request_msg,
                model_used='lead-gatekeeper',
                action_type='lead_form'
            )
            return JsonResponse({
                'success': True,
                'reply': lead_request_msg,
                'action_type': 'lead_form',
                'model_used': 'lead-gatekeeper',
                'has_lead': False,
                'metadata': {},
                'created_at': bot_msg.created_at.isoformat(),
            })

        # 4. Lead is Secured: Check for Booking Intent
        msg_lower = user_message.lower()
        booking_signals = ['book', 'appointment', 'schedule', 'consultation', 'discovery call', 'meet with you', 'strategy session', 'available slot']
        if any(sig in msg_lower for sig in booking_signals):
            session.status = 'booking_initiated'
            session.save(update_fields=['status'])

            upcoming_options = find_next_available_dates(4)
            reply_text = (
                f"I would be glad to arrange a 1-hour discovery consultation for you, {session.lead.full_name}! "
                "Our sessions are conducted Sunday to Friday between 8:00 AM and 8:00 PM East Africa Time (EAT, closed Saturdays) "
                "via Google Meet, WhatsApp Call, or in-person at our Nairobi CBD headquarters. "
                "Please choose your preferred upcoming date and window below:"
            )
            bot_msg = ChatMessage.objects.create(
                session=session,
                sender='assistant',
                message=reply_text,
                model_used='booking-scheduler',
                action_type='slot_picker',
                metadata={'dates': upcoming_options}
            )
            return JsonResponse({
                'success': True,
                'reply': reply_text,
                'action_type': 'slot_picker',
                'model_used': 'booking-scheduler',
                'has_lead': True,
                'metadata': {'dates': upcoming_options},
                'created_at': bot_msg.created_at.isoformat(),
            })

        # 4. Standard Inquiry: Pass to Gemini Multi-Model Cascade
        client_context = {
            'name': session.lead.full_name,
            'email': session.lead.email,
            'phone': session.lead.phone,
            'industry': session.lead.industry,
        }
        
        # Pull recent message history for context
        history = list(session.messages.order_by('-created_at')[:8])
        history.reverse()
        history_dicts = [{'sender': m.sender, 'message': m.message} for m in history if m.sender in ['user', 'assistant']]

        ai_result = generate_conversational_response(history_dicts, user_message, client_context)

        bot_msg = ChatMessage.objects.create(
            session=session,
            sender='assistant',
            message=ai_result['text'],
            model_used=ai_result['model_used'],
            is_fallback=ai_result['is_fallback'],
            action_type='normal',
            metadata={'errors': ai_result.get('error_logs', [])}
        )

        return JsonResponse({
            'success': True,
            'reply': ai_result['text'],
            'action_type': 'normal',
            'model_used': ai_result['model_used'],
            'is_fallback': ai_result['is_fallback'],
            'has_lead': True,
            'metadata': {},
            'created_at': bot_msg.created_at.isoformat(),
        })


class CaptureLeadApiView(View):
    """
    Validates prospect contact details, registers LeadCapture, dispatches welcome & admin alerts,
    and immediately fulfills pending query if present.
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

        session_id = data.get('session_id')
        full_name = (data.get('full_name') or '').strip()
        email = (data.get('email') or '').strip().lower()
        phone = (data.get('phone') or '').strip()
        industry = (data.get('industry') or '').strip()
        bottleneck = (data.get('business_bottleneck') or '').strip()

        if not session_id or not full_name or not email or not phone:
            return JsonResponse({'success': False, 'error': 'Full Name, Email, and Phone are required.'}, status=400)

        if not re.match(EMAIL_REGEX, email):
            return JsonResponse({'success': False, 'error': 'Please enter a valid email address.'}, status=400)

        clean_digits = ''.join(c for c in phone if c.isdigit())
        if len(clean_digits) < 7:
            return JsonResponse({'success': False, 'error': 'Please provide a valid WhatsApp/Phone number with country code.'}, status=400)

        session = get_object_or_404(ChatSession, session_id=session_id)

        # Create or update LeadCapture profile
        lead, _ = LeadCapture.objects.get_or_create(
            email=email,
            defaults={
                'full_name': full_name,
                'phone': phone,
                'industry': industry,
                'business_bottleneck': bottleneck,
            }
        )
        lead.full_name = full_name
        lead.phone = phone
        if industry:
            lead.industry = industry
        if bottleneck:
            lead.business_bottleneck = bottleneck
        lead.save()

        session.lead = lead
        session.status = 'lead_captured'
        session.save(update_fields=['lead', 'status'])

        # Send Real-Time Internal Admin Alert (safely so SMTP timeouts never block HTTP response)
        try:
            send_lead_admin_alert_email(lead, session)
        except Exception as e:
            logger.warning(f"Could not send admin alert email: {e}")

        # Fulfill pending query if user asked something before submitting details
        pending_query = session.pending_query.strip()
        if pending_query:
            session.pending_query = ''
            session.save(update_fields=['pending_query'])

            client_context = {'name': lead.full_name, 'email': lead.email, 'phone': lead.phone, 'industry': lead.industry}
            ai_result = generate_conversational_response([], pending_query, client_context)

            fulfilled_reply = (
                f"Thank you, {lead.full_name}! Your contact details have been securely recorded. "
                f"Regarding your question about **\"{pending_query}\"**:\n\n"
                f"{ai_result['text']}\n\n"
                "Would you like to schedule a free 1-on-1 technical discovery call with our solutions engineering team?"
            )

            ChatMessage.objects.create(
                session=session,
                sender='assistant',
                message=fulfilled_reply,
                model_used=ai_result['model_used'],
                is_fallback=ai_result['is_fallback'],
                action_type='normal'
            )

            # Also email the initial transcript & recommendations
            send_lead_transcript_email(lead, session, request)

            return JsonResponse({
                'success': True,
                'has_lead': True,
                'lead_name': lead.full_name,
                'reply': fulfilled_reply,
                'action_type': 'normal',
                'model_used': ai_result['model_used'],
                'created_at': timezone.now().isoformat(),
            })

        # No pending query: present curated introductory discovery options
        welcome_reply = (
            f"Thank you, {lead.full_name}! It's great to meet you. "
            "Our engineering desk in Nairobi specializes in deploying high-performance digital systems.\n\n"
            "Here are our most requested digital growth systems:\n"
            "• **24/7 AI WhatsApp Qualification Agents** (Turn conversations into booked appointments)\n"
            "• **Custom Web Applications & SaaS** (Django & modern stacks engineered for sub-second speeds)\n"
            "• **Healthcare & Clinic Management Platforms** (EMR, patient queues, M-Pesa billing)\n"
            "• **Retail & E-Commerce Engines** (M-Pesa Daraja STK Push & international checkout)\n\n"
            "What specific challenge or system can we help you engineer?"
        )
        ChatMessage.objects.create(
            session=session,
            sender='assistant',
            message=welcome_reply,
            model_used='system-desk',
            action_type='normal'
        )

        return JsonResponse({
            'success': True,
            'has_lead': True,
            'lead_name': lead.full_name,
            'reply': welcome_reply,
            'action_type': 'normal',
            'model_used': 'system-desk',
            'created_at': timezone.now().isoformat(),
        })


class CheckAvailabilityApiView(View):
    """
    Returns available consultation time-slots for a specific calendar date.
    """
    def get(self, request):
        date_str = request.GET.get('date', '').strip()
        if not date_str:
            return JsonResponse({'success': False, 'error': 'date parameter (YYYY-MM-DD) is required'}, status=400)

        try:
            target_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format. Expected YYYY-MM-DD.'}, status=400)

        availability = get_available_slots_for_date(target_date)
        return JsonResponse({'success': True, 'data': availability})


class BookConsultationApiView(View):
    """
    Books an appointment directly via the AI assistant, links it to the lead,
    and dispatches confirmation emails with calendar .ics attachment.
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

        session_id = data.get('session_id')
        date_str = data.get('date')
        slot_key = data.get('slot_key') or data.get('slot')
        meeting_type = data.get('meeting_type', 'google_meet')
        service_id = data.get('service_id')
        description = data.get('description', 'AI Consultation discovery session')

        if not session_id or not date_str or not slot_key:
            return JsonResponse({'success': False, 'error': 'session_id, date, and slot_key are required.'}, status=400)

        session = get_object_or_404(ChatSession, session_id=session_id)
        if not session.lead:
            return JsonResponse({'success': False, 'error': 'Please provide contact details before scheduling.'}, status=400)

        try:
            preferred_date = datetime.date.fromisoformat(date_str)
            if preferred_date < timezone.now().date():
                return JsonResponse({'success': False, 'error': 'Please choose an upcoming calendar date.'}, status=400)
            if preferred_date.weekday() == 5:
                return JsonResponse({'success': False, 'error': 'UniqueTechCamp is closed on Saturdays. Consultations are available Sunday through Friday.'}, status=400)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid date format provided.'}, status=400)

        # Check if slot is taken
        already_taken = Appointment.objects.filter(
            preferred_date=preferred_date,
            preferred_time_slot=slot_key,
            status__in=['pending', 'confirmed']
        ).exists()

        if already_taken:
            return JsonResponse({
                'success': False,
                'error': f"The slot '{slot_key}' on {date_str} is already reserved. Please select another slot."
            }, status=409)

        service = None
        if service_id:
            try:
                service = Service.objects.filter(id=service_id, is_active=True).first()
            except Exception:
                pass

        lead = session.lead

        # Create Appointment Record attributed to AI Assistant
        appointment = Appointment.objects.create(
            service=service,
            full_name=lead.full_name,
            email=lead.email,
            phone=lead.phone,
            company_name=lead.industry or '',
            preferred_date=preferred_date,
            preferred_time_slot=slot_key,
            meeting_type=meeting_type,
            project_description=description,
            status='pending',
            source='ai_assistant',
        )

        lead.associated_appointment = appointment
        lead.save(update_fields=['associated_appointment'])

        session.status = 'appointment_booked'
        session.save(update_fields=['status'])

        # Dispatch robust notifications (Client Confirmation + .ics calendar invite + Admin Alert)
        send_appointment_emails(appointment, request)

        # In-chat confirmation message with card payload
        confirmation_msg = (
            f"🎉 **Consultation Successfully Confirmed!**\n\n"
            f"• **Reference**: `{appointment.booking_reference}`\n"
            f"• **Client**: {appointment.full_name}\n"
            f"• **Date**: {appointment.preferred_date.strftime('%A, %B %d, %Y')}\n"
            f"• **Time**: {appointment.preferred_time_slot} (EAT / Nairobi)\n"
            f"• **Meeting Platform**: {appointment.meeting_type_display_name}\n\n"
            "An official calendar invite (.ics) and confirmation email have been dispatched to your inbox. "
            "Our engineering team will meet you at the scheduled time."
        )

        card_meta = {
            'reference': appointment.booking_reference,
            'date': str(appointment.preferred_date),
            'time': appointment.preferred_time_slot,
            'channel': appointment.meeting_type_display_name,
            'service': appointment.service_name,
            'whatsapp_url': f"https://wa.me/254715479955?text=Hello%20UniqueTechCamp!%20I%20have%20booked%20consultation%20{appointment.booking_reference}.",
        }

        bot_msg = ChatMessage.objects.create(
            session=session,
            sender='assistant',
            message=confirmation_msg,
            model_used='system-desk',
            action_type='booking_card',
            metadata=card_meta
        )

        # Dispatch updated transcript to client
        send_lead_transcript_email(lead, session, request)

        return JsonResponse({
            'success': True,
            'reply': confirmation_msg,
            'action_type': 'booking_card',
            'metadata': card_meta,
            'created_at': bot_msg.created_at.isoformat(),
        })


class EmailTranscriptApiView(View):
    """
    Explicitly triggers emailing of the session transcript upon client request or session completion.
    """
    def post(self, request):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

        session_id = data.get('session_id')
        session = get_object_or_404(ChatSession, session_id=session_id)

        lead = session.lead
        if not lead and request.user.is_authenticated:
            phone = request.user.profile.phone if hasattr(request.user, 'profile') and request.user.profile.phone else ''
            lead, _ = LeadCapture.objects.get_or_create(
                email=request.user.email,
                defaults={
                    'full_name': request.user.get_full_name() or request.user.username,
                    'phone': phone,
                }
            )
            session.lead = lead
            session.save(update_fields=['lead'])

        if not lead or not lead.email:
            return JsonResponse({'success': False, 'error': 'Please provide your contact details in the chat first so we know where to send your transcript.'}, status=400)

        sent = send_lead_transcript_email(lead, session, request)
        if sent:
            return JsonResponse({'success': True, 'message': f"Transcript successfully sent to {lead.email}"})
        return JsonResponse({'success': False, 'error': 'Could not dispatch transcript email. Please check your email address.'}, status=500)
