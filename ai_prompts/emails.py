import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from marketing.email_service import send_robust_email

logger = logging.getLogger(__name__)

def send_prompt_access_approved_email(purchase):
    """
    Sends the official confirmation email to the client when their payment
    is verified by Management in Django Admin, granting access to the prompt.
    """
    if not purchase or not purchase.client_email:
        return False

    prompt = purchase.prompt
    access_url = f"https://uniquetechcamp.org/ai-project-prompts/{prompt.slug}/"
    subject = f"✅ Access Unlocked: {prompt.title} — UniqueTechCamp"

    context = {
        'purchase': purchase,
        'prompt': prompt,
        'access_url': access_url,
        'site_url': 'https://uniquetechcamp.org',
        'support_phone': '+254 715 479 955',
    }

    try:
        html_content = render_to_string('emails/prompt_access_approved.html', context)
        text_content = strip_tags(html_content)

        success, _ = send_robust_email(
            to_email=purchase.client_email,
            subject=subject,
            body_text=text_content,
            body_html=html_content,
            sender_choice='email1',
            recipient_name=purchase.client_name,
            email_type='prompt_purchase_approved',
        )
        return success
    except Exception as e:
        logger.error(f"Failed to send prompt access approval email to {purchase.client_email}: {e}")
        return False


def send_prompt_purchase_admin_alert(purchase):
    """
    Alerts UniqueTechCamp Management that a client has submitted payment proof
    requiring review and verification in Django Admin.
    """
    if not purchase:
        return False

    admin_recipients = [
        getattr(settings, 'ADMIN_EMAIL_PRIMARY', 'info@uniquetechcamp.org'),
        getattr(settings, 'ADMIN_EMAIL_GMAIL', 'UniqueTechCamp@gmail.com'),
    ]

    prompt = purchase.prompt
    subject = f"🚨 [Prompt Payment Review] {purchase.client_name} — {prompt.title}"

    context = {
        'purchase': purchase,
        'prompt': prompt,
        'site_url': 'https://uniquetechcamp.org',
    }

    try:
        html_content = render_to_string('emails/prompt_purchase_admin_alert.html', context)
        text_content = strip_tags(html_content)

        for admin_email in admin_recipients:
            send_robust_email(
                to_email=admin_email,
                subject=subject,
                body_text=text_content,
                body_html=html_content,
                sender_choice='email1',
                recipient_name='UniqueTechCamp Admin',
                email_type='prompt_payment_alert',
            )
        return True
    except Exception as e:
        logger.error(f"Failed to dispatch prompt purchase admin alert: {e}")
        return False
