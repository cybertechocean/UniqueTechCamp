import time
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.db import close_old_connections
from .models import BulkCampaign, CampaignRecipient

logger = logging.getLogger(__name__)

def render_campaign_email_content(format_type, recipient_name, subject, message, campaign):
    """
    Renders the HTML and plaintext body based on chosen email_format:
    - 'welcome': Official High-Converting Welcome Email Layout (emails/welcome_email.html)
    - 'branded': UniqueTechCamp Branded Layout (emails/marketing_campaign_email.html)
    - 'plain': Clean Direct Message (Minimalist Text, no HTML wrapper)
    """
    fmt = getattr(campaign, 'email_format', format_type) or format_type or 'branded'
    if fmt == 'welcome':
        context = {
            'user_name': recipient_name or 'Valued Client',
            'cta_url': 'https://uniquetechcamp.org/services/',
            'cta_text': 'Explore 165+ Growth Services →',
            'site_url': 'https://uniquetechcamp.org',
            'logo_url': 'https://uniquetechcamp.org/static/images/logo-rounded.png',
            'custom_message': message,
            'campaign': campaign,
        }
        html_content = render_to_string('emails/welcome_email.html', context)
        text_content = strip_tags(html_content) if html_content else message
    elif fmt == 'plain':
        html_content = None
        text_content = message
    else:  # 'branded'
        context = {
            'recipient_name': recipient_name,
            'subject': subject,
            'message': message,
            'campaign': campaign,
            'website_url': 'https://uniquetechcamp.org',
            'logo_url': 'https://uniquetechcamp.org/static/images/logo-rounded.png',
        }
        html_content = render_to_string('emails/marketing_campaign_email.html', context)
        text_content = strip_tags(html_content)

    return text_content, html_content


def send_single_campaign_email(recipient, from_email=None):
    """
    Renders and dispatches a single personalized email for a campaign recipient.
    Returns (True, None) on success, or (False, error_str) on failure.
    """
    from .email_service import send_robust_email

    try:
        text_content, html_content = render_campaign_email_content(
            getattr(recipient.campaign, 'email_format', 'branded'),
            recipient_name=recipient.name,
            subject=recipient.subject,
            message=recipient.personalized_message,
            campaign=recipient.campaign
        )

        sender_choice = getattr(recipient.campaign, 'sender_choice', 'email1') or 'email1'
        if not from_email:
            from_email = f"{recipient.campaign.sender_name} <{recipient.campaign.sender_email}>"

        success, log = send_robust_email(
            to_email=recipient.email,
            subject=recipient.subject,
            body_text=text_content,
            body_html=html_content,
            sender_choice=sender_choice,
            from_email=from_email,
            recipient_name=recipient.name,
            email_type='campaign',
        )

        if success:
            recipient.status = 'sent'
            recipient.sent_at = timezone.now()
            recipient.error_message = ''
            recipient.save(update_fields=['status', 'sent_at', 'error_message'])
            return True, None
        else:
            err_msg = log.error_message if log else "Delivery failed"
            recipient.status = 'failed'
            recipient.error_message = err_msg[:500]
            recipient.save(update_fields=['status', 'error_message'])
            return False, err_msg

    except Exception as e:
        err_msg = str(e)
        logger.error(f"Failed to dispatch marketing email to {recipient.email}: {err_msg}")
        recipient.status = 'failed'
        recipient.error_message = err_msg[:500]
        recipient.save(update_fields=['status', 'error_message'])
        return False, err_msg



def dispatch_next_campaign_recipient(campaign):
    """
    Dispatches the next single pending recipient for a campaign.
    Updates campaign counts immediately.
    Returns a dict with execution results for API response or worker consumption.
    """
    close_old_connections()
    recipient = campaign.recipients.filter(status='pending').first()

    if not recipient:
        # All recipients processed
        sent_c = campaign.recipients.filter(status='sent').count()
        failed_c = campaign.recipients.filter(status='failed').count()
        campaign.sent_count = sent_c
        campaign.failed_count = failed_c
        campaign.status = 'completed'
        if not campaign.completed_at:
            campaign.completed_at = timezone.now()
        campaign.save(update_fields=['sent_count', 'failed_count', 'status', 'completed_at'])
        close_old_connections()
        return {
            'completed': True,
            'recipient': None,
            'sent_count': campaign.sent_count,
            'failed_count': campaign.failed_count,
            'total_recipients': campaign.total_recipients,
            'progress_percentage': campaign.progress_percentage,
            'remaining_count': 0,
        }

    # Ensure campaign status reflects sending
    if campaign.status != 'sending':
        campaign.status = 'sending'
        campaign.save(update_fields=['status'])

    from_email = f"{campaign.sender_name} <{campaign.sender_email}>"
    success, err_msg = send_single_campaign_email(recipient, from_email=from_email)

    # Recalculate and persist counts immediately
    sent_c = campaign.recipients.filter(status='sent').count()
    failed_c = campaign.recipients.filter(status='failed').count()
    remaining_c = campaign.recipients.filter(status='pending').count()

    campaign.sent_count = sent_c
    campaign.failed_count = failed_c
    if remaining_c == 0:
        campaign.status = 'completed'
        campaign.completed_at = timezone.now()
        campaign.save(update_fields=['sent_count', 'failed_count', 'status', 'completed_at'])
    else:
        campaign.save(update_fields=['sent_count', 'failed_count'])

    close_old_connections()

    return {
        'completed': remaining_c == 0,
        'recipient_id': recipient.id,
        'recipient_name': recipient.name,
        'recipient_email': recipient.email,
        'recipient_status': recipient.status,
        'error_message': recipient.error_message,
        'sent_at': recipient.sent_at.strftime('%b %d, %H:%M:%S') if recipient.sent_at else '',
        'sent_count': campaign.sent_count,
        'failed_count': campaign.failed_count,
        'total_recipients': campaign.total_recipients,
        'progress_percentage': campaign.progress_percentage,
        'remaining_count': remaining_c,
        'delay_seconds': campaign.delay_seconds,
    }


def execute_campaign(campaign_id):
    """
    Runs the bulk sending loop with configurable delay between each email.
    Can be invoked synchronously or via background thread/task/CLI.
    """
    close_old_connections()
    try:
        campaign = BulkCampaign.objects.get(id=campaign_id)
    except BulkCampaign.DoesNotExist:
        logger.error(f"Campaign with ID {campaign_id} not found.")
        return 0, 0

    campaign.status = 'sending'
    campaign.save(update_fields=['status'])

    from_email = f"{campaign.sender_name} <{campaign.sender_email}>"

    try:
        while True:
            close_old_connections()
            # Check if campaign was paused or reset by user
            campaign.refresh_from_db()
            if campaign.status != 'sending':
                logger.info(f"Campaign {campaign.campaign_id} dispatch stopped: status changed to {campaign.status}")
                break

            recipient = campaign.recipients.filter(status='pending').first()
            if not recipient:
                break

            success, _ = send_single_campaign_email(recipient, from_email=from_email)

            # Persist counts immediately after every single send
            campaign.sent_count = campaign.recipients.filter(status='sent').count()
            campaign.failed_count = campaign.recipients.filter(status='failed').count()
            campaign.save(update_fields=['sent_count', 'failed_count'])

            remaining = campaign.recipients.filter(status='pending').count()
            if remaining == 0:
                break

            # Apply configurable delay time
            if campaign.delay_seconds > 0:
                time.sleep(campaign.delay_seconds)

    except Exception as e:
        logger.error(f"Unexpected error executing campaign {campaign_id}: {e}", exc_info=True)
    finally:
        close_old_connections()
        campaign.refresh_from_db()
        pending_left = campaign.recipients.filter(status='pending').count()
        if pending_left == 0:
            campaign.status = 'completed'
            campaign.completed_at = timezone.now()
        campaign.sent_count = campaign.recipients.filter(status='sent').count()
        campaign.failed_count = campaign.recipients.filter(status='failed').count()
        campaign.save(update_fields=['sent_count', 'failed_count', 'status', 'completed_at'])
        close_old_connections()

    logger.info(f"Campaign {campaign.campaign_id} dispatch ended. Sent: {campaign.sent_count}, Failed: {campaign.failed_count}")
    return campaign.sent_count, campaign.failed_count


def send_test_email(campaign, target_email):
    """
    Dispatches a single test email using the campaign's 1st recipient or default preview.
    Allows the user to inspect subject, formatting, and layout in their personal inbox before firing the batch.
    """
    from_email = f"{campaign.sender_name} <{campaign.sender_email}>"
    first_recipient = campaign.recipients.first()

    sample_name = first_recipient.name if first_recipient else "Valued Client"
    sample_subject = f"[TEST PREVIEW] {first_recipient.subject if first_recipient else campaign.default_subject}"
    sample_message = first_recipient.personalized_message if first_recipient else (
        "Hello,\n\nThis is a live test preview of your personalized broadcast message sent from the UniqueTechCamp Marketing Engine.\n\nAll formatting, typography, and consultation booking CTAs are verified."
    )

    text_content, html_content = render_campaign_email_content(
        getattr(campaign, 'email_format', 'branded'),
        recipient_name=sample_name,
        subject=sample_subject,
        message=sample_message,
        campaign=campaign
    )

    from .email_service import send_robust_email
    sender_choice = getattr(campaign, 'sender_choice', 'email1') or 'email1'
    success, _ = send_robust_email(
        to_email=target_email,
        subject=sample_subject,
        body_text=text_content,
        body_html=html_content,
        sender_choice=sender_choice,
        from_email=from_email,
        recipient_name=sample_name,
        email_type='campaign',
    )
    return success

