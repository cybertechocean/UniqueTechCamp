"""
Email dispatch utilities for UniqueTechCamp.
Handles branded HTML emails with top company logo and bottom social media icon links.
"""

import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

logger = logging.getLogger(__name__)

DEFAULT_FROM = getattr(settings, 'DEFAULT_FROM_EMAIL', 'UniqueTechCamp Web Developers <info@uniquetechcamp.org>')
DEFAULT_SITE_URL = "https://uniquetechcamp.org"
DEFAULT_LOGO_URL = "https://uniquetechcamp.org/static/images/logo-rounded.png"


def get_email_context(request=None):
    """
    Returns standard branding context for email templates.
    """
    if request:
        protocol = "https" if request.is_secure() else "http"
        domain = request.get_host()
        site_url = f"{protocol}://{domain}"
        logo_url = f"{site_url}/static/images/logo-rounded.png"
    else:
        protocol = "https"
        domain = "uniquetechcamp.org"
        site_url = DEFAULT_SITE_URL
        logo_url = DEFAULT_LOGO_URL

    return {
        "protocol": protocol,
        "domain": domain,
        "site_url": site_url,
        "logo_url": logo_url,
    }


def send_welcome_email(recipient_email, user_name=None, user=None, temporary_password=None, cta_url=None, request=None):
    """
    Sends a high-converting, branded welcome email with the UniqueTechCamp logo at the top
    and 9 social media channels at the bottom.
    """
    context = get_email_context(request)
    
    if user:
        user_name = user_name or user.get_full_name() or user.username
        recipient_email = recipient_email or user.email

    context.update({
        "user_name": user_name or "Valued Client",
        "user": user,
        "temporary_password": temporary_password,
        "cta_url": cta_url or f"{context['site_url']}/services/",
        "cta_text": "Explore 107 Growth Services →",
    })

    subject = "Welcome to UniqueTechCamp — Website, Clients, Income"
    
    try:
        html_content = render_to_string("emails/welcome_email.html", context)
        text_content = render_to_string("emails/welcome_email.txt", context)
    except Exception:
        # Fallback to plain text rendering
        html_content = render_to_string("emails/welcome_email.html", context)
        text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=DEFAULT_FROM,
        to=[recipient_email]
    )
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send(fail_silently=False)
        logger.info(f"Welcome email successfully sent to {recipient_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {recipient_email}: {e}")
        return False


def send_password_reset_email(user, request=None):
    """
    Sends a branded password reset email with the UniqueTechCamp logo at the top,
    one-click reset button, and social media channels at the bottom.
    """
    if not user.email:
        logger.warning(f"User {user.username} has no email address for password reset.")
        return False

    context = get_email_context(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    reset_url = f"{context['site_url']}/auth/reset/{uid}/{token}/"

    context.update({
        "user": user,
        "email": user.email,
        "uid": uid,
        "token": token,
        "reset_url": reset_url,
    })

    subject = "Password Reset Request | UniqueTechCamp"
    
    try:
        html_content = render_to_string("emails/password_reset_email.html", context)
        text_content = render_to_string("emails/password_reset_email.txt", context)
    except Exception:
        html_content = render_to_string("registration/password_reset_email.html", context)
        text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=DEFAULT_FROM,
        to=[user.email]
    )
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send(fail_silently=False)
        logger.info(f"Password reset email successfully sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email to {user.email}: {e}")
        return False
