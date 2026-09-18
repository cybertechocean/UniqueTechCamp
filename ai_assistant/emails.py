import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from marketing.email_service import send_robust_email

logger = logging.getLogger(__name__)

def send_lead_transcript_email(lead, session, request=None):
    """
    Emails the complete branded consultation transcript and strategic recommendations
    to the prospective client.
    """
    if not lead or not lead.email:
        return False

    try:
        messages = session.messages.order_by('created_at') if session else []
        subject = f"Your UniqueTechCamp AI Consultation Summary & Recommendations"
        
        context = {
            'lead': lead,
            'session': session,
            'messages': messages,
            'website_url': 'https://uniquetechcamp.org',
            'whatsapp_phone': '254715479955',
        }
        
        html_content = render_to_string('emails/ai_lead_transcript.html', context)
        text_content = strip_tags(html_content)

        success = send_robust_email(
            to_email=lead.email,
            subject=subject,
            body_text=text_content,
            body_html=html_content,
            sender_choice='email1',
            recipient_name=lead.full_name,
            email_type='ai_transcript',
        )

        if success:
            lead.transcript_sent = True
            lead.transcript_sent_at = timezone.now()
            lead.save(update_fields=['transcript_sent', 'transcript_sent_at'])
            logger.info(f"AI Consultation Transcript successfully sent to client: {lead.email}")
        return success
    except Exception as e:
        logger.error(f"Failed to dispatch AI Consultation Transcript to {lead.email}: {e}")
        return False


def send_lead_admin_alert_email(lead, session, appointment=None):
    """
    Dispatches a real-time high-priority acquisition alert to the UniqueTechCamp engineering desk.
    """
    if not lead:
        return False

    admin_recipients = [
        getattr(settings, 'ADMIN_EMAIL_PRIMARY', 'info@uniquetechcamp.org'),
        getattr(settings, 'ADMIN_EMAIL_GMAIL', 'UniqueTechCamp@gmail.com'),
    ]

    try:
        messages = session.messages.order_by('created_at') if session else []
        subject = f"🚨 [High Priority Lead] {lead.full_name} - AI Acquisition Desk"
        
        context = {
            'lead': lead,
            'session': session,
            'messages': messages,
            'appointment': appointment,
        }
        
        html_content = render_to_string('emails/ai_lead_admin_alert.html', context)
        text_content = strip_tags(html_content)

        for admin_email in admin_recipients:
            send_robust_email(
                to_email=admin_email,
                subject=subject,
                body_text=text_content,
                body_html=html_content,
                sender_choice='email1',
                recipient_name='UniqueTechCamp Admin',
                email_type='ai_lead_alert',
            )

        lead.admin_alert_sent = True
        lead.admin_alert_sent_at = timezone.now()
        lead.save(update_fields=['admin_alert_sent', 'admin_alert_sent_at'])
        logger.info(f"AI Lead Acquisition alert dispatched for {lead.full_name} ({lead.email})")
        return True
    except Exception as e:
        logger.error(f"Failed to dispatch admin AI lead alert: {e}")
        return False
