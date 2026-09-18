import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from core.emails import get_email_context

logger = logging.getLogger(__name__)


def send_verification_email(user, request=None):
    """
    Sends an ultra-modern branded email verification link to newly registered clients.
    Features the UniqueTechCamp logo at the top and 9 official social channels at the bottom.
    """
    if not user.email:
        logger.warning(f"Cannot send verification email: User {user.username} has no email.")
        return False

    profile = getattr(user, 'profile', None)
    if not profile:
        from .models import UserProfile
        profile = UserProfile.objects.create(user=user)

    token = profile.generate_new_verification_token()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    context = get_email_context(request)

    verification_url = f"{context['site_url']}/account/verify-email/{uid}/{token}/"

    context.update({
        "user": user,
        "user_name": user.get_full_name() or user.username,
        "verification_url": verification_url,
        "token": token,
        "email": user.email,
        "support_email": "info@uniquetechcamp.org",
        "phone_number": "+254 715 479 955",
    })

    subject = "Verify Your Email Address | UniqueTechCamp Client Account"

    try:
        html_content = render_to_string("accounts/emails/verify_email.html", context)
        text_content = render_to_string("accounts/emails/verify_email.txt", context)
    except Exception:
        try:
            html_content = render_to_string("accounts/emails/verify_email.html", context)
            text_content = strip_tags(html_content)
        except Exception as e:
            logger.error(f"Error rendering verification email templates: {e}")
            text_content = f"Hello {user.get_full_name() or user.username},\n\nPlease verify your email for UniqueTechCamp by clicking: {verification_url}\n\nThank you,\nUniqueTechCamp Team"
            html_content = f"<p>Hello {user.get_full_name() or user.username},</p><p>Please verify your email: <a href='{verification_url}'>Verify Account</a></p>"

    try:
        from marketing.email_service import send_robust_email
        success, msg = send_robust_email(
            to_email=user.email,
            subject=subject,
            body_text=text_content,
            body_html=html_content,
            sender_choice='email1',
            recipient_name=user.get_full_name() or user.username,
            email_type='system'
        )
        return success
    except Exception as e:
        logger.error(f"Failed to send email verification to {user.email}: {e}")
        return False
