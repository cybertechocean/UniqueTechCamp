import time
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from .models import BulkCampaign, CampaignRecipient

logger = logging.getLogger(__name__)

def send_single_campaign_email(recipient, from_email=None):
    """
    Renders and dispatches a single personalized email for a campaign recipient.
    Returns (True, None) on success, or (False, error_str) on failure.
    """
    if not from_email:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'UniqueTechCamp Web Developers <info@uniquetechcamp.org>')

    try:
        context = {
            'recipient_name': recipient.name,
            'subject': recipient.subject,
            'message': recipient.personalized_message,
            'campaign': recipient.campaign,
            'website_url': 'https://uniquetechcamp.org',
        }
        html_content = render_to_string('emails/marketing_campaign_email.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=recipient.subject,
            body=text_content,
            from_email=from_email,
            to=[recipient.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        recipient.status = 'sent'
        recipient.sent_at = timezone.now()
        recipient.error_message = ''
        recipient.save(update_fields=['status', 'sent_at', 'error_message'])
        return True, None

    except Exception as e:
        err_msg = str(e)
        logger.error(f"Failed to dispatch marketing email to {recipient.email}: {err_msg}")
        recipient.status = 'failed'
        recipient.error_message = err_msg[:500]
        recipient.save(update_fields=['status', 'error_message'])
        return False, err_msg


def execute_campaign(campaign_id):
    """
    Runs the bulk sending loop with configurable delay between each email.
    Can be invoked synchronously or via background thread/task.
    """
    try:
        campaign = BulkCampaign.objects.get(id=campaign_id)
    except BulkCampaign.DoesNotExist:
        logger.error(f"Campaign with ID {campaign_id} not found.")
        return

    campaign.status = 'sending'
    campaign.save(update_fields=['status'])

    pending_recipients = campaign.recipients.filter(status='pending')
    from_email = f"{campaign.sender_name} <{campaign.sender_email}>"

    sent_count = campaign.sent_count
    failed_count = campaign.failed_count

    for idx, recipient in enumerate(pending_recipients):
        success, _ = send_single_campaign_email(recipient, from_email=from_email)
        if success:
            sent_count += 1
        else:
            failed_count += 1

        # Update campaign counts incrementally every 5 sends or on completion
        if (idx + 1) % 5 == 0 or (idx + 1) == len(pending_recipients):
            campaign.sent_count = sent_count
            campaign.failed_count = failed_count
            campaign.save(update_fields=['sent_count', 'failed_count'])

        # Apply configurable delay time
        if campaign.delay_seconds > 0 and (idx + 1) < len(pending_recipients):
            time.sleep(campaign.delay_seconds)

    campaign.sent_count = sent_count
    campaign.failed_count = failed_count
    campaign.status = 'completed' if failed_count == 0 else 'completed'
    campaign.completed_at = timezone.now()
    campaign.save(update_fields=['sent_count', 'failed_count', 'status', 'completed_at'])

    logger.info(f"Campaign {campaign.campaign_id} finished. Sent: {sent_count}, Failed: {failed_count}")
    return sent_count, failed_count


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

    context = {
        'recipient_name': sample_name,
        'subject': sample_subject,
        'message': sample_message,
        'campaign': campaign,
        'website_url': 'https://uniquetechcamp.org',
    }
    html_content = render_to_string('emails/marketing_campaign_email.html', context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=sample_subject,
        body=text_content,
        from_email=from_email,
        to=[target_email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
    return True
