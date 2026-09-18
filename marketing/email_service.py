import os
import mimetypes
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.utils import timezone
from .models import EmailLog

logger = logging.getLogger(__name__)

def get_sender_from_email(sender_choice='email1'):
    """
    Returns the appropriate From: header based on sender selection.
    """
    if sender_choice == 'email2':
        return getattr(settings, 'EMAIL2_FROM_EMAIL', 'UniqueTechCamp <UniqueTechCamp@gmail.com>')
    return getattr(settings, 'EMAIL1_FROM_EMAIL', 'UniqueTechCamp Solutions <info@uniquetechcamp.org>')


def get_email_connection(sender_choice='email1', port_override=None, ssl_override=None, tls_override=None):
    """
    Instantiates and returns the SMTP EmailBackend for the requested sender,
    or test in-memory connection if running tests.
    """
    if getattr(settings, 'EMAIL_BACKEND', '').endswith('locmem.EmailBackend'):
        from django.core.mail import get_connection
        return get_connection()

    if sender_choice == 'email2':
        host = getattr(settings, 'EMAIL2_HOST', 'smtp.gmail.com')
        port = port_override if port_override is not None else getattr(settings, 'EMAIL2_PORT', 465)
        username = getattr(settings, 'EMAIL2_HOST_USER', 'UniqueTechCamp@gmail.com')
        raw_pwd = getattr(settings, 'EMAIL2_HOST_PASSWORD', '')
        password = str(raw_pwd).replace(' ', '').strip().strip('"').strip("'")
        if ssl_override is not None:
            use_ssl = ssl_override
            use_tls = tls_override if tls_override is not None else not ssl_override
        else:
            use_ssl = getattr(settings, 'EMAIL2_USE_SSL', True)
            use_tls = getattr(settings, 'EMAIL2_USE_TLS', False)
    else:
        # Email 1: Primary (info@uniquetechcamp.org)
        host = getattr(settings, 'EMAIL1_HOST', 'mail.uniquetechcamp.org')
        port = port_override if port_override is not None else getattr(settings, 'EMAIL1_PORT', 465)
        username = getattr(settings, 'EMAIL1_HOST_USER', 'info@uniquetechcamp.org')
        raw_pwd1 = getattr(settings, 'EMAIL1_HOST_PASSWORD', '')
        password = str(raw_pwd1).strip().strip('"').strip("'") if raw_pwd1 else ''
        if ssl_override is not None:
            use_ssl = ssl_override
            use_tls = tls_override if tls_override is not None else not ssl_override
        else:
            use_ssl = getattr(settings, 'EMAIL1_USE_SSL', True)
            use_tls = getattr(settings, 'EMAIL1_USE_TLS', False)

        # Graceful fallback: If Email 1 password is empty, route through Google App Password SMTP
        if not password:
            host = getattr(settings, 'EMAIL2_HOST', 'smtp.gmail.com')
            port = port_override if port_override is not None else getattr(settings, 'EMAIL2_PORT', 465)
            username = getattr(settings, 'EMAIL2_HOST_USER', 'UniqueTechCamp@gmail.com')
            raw_pwd = getattr(settings, 'EMAIL2_HOST_PASSWORD', '')
            password = str(raw_pwd).replace(' ', '').strip().strip('"').strip("'")
            use_ssl = getattr(settings, 'EMAIL2_USE_SSL', True)
            use_tls = getattr(settings, 'EMAIL2_USE_TLS', False)

    return EmailBackend(
        host=host,
        port=port,
        username=username,
        password=password,
        use_tls=use_tls,
        use_ssl=use_ssl,
        fail_silently=False,
        timeout=25,
    )


def send_robust_email(
    to_email,
    subject,
    body_text,
    body_html=None,
    sender_choice='email1',
    from_email=None,
    recipient_name='',
    attachment_file=None,
    attachment_content=None,
    attachment_filename='',
    attachment_content_type=None,
    email_type='single',
    existing_log=None,
):
    """
    Robust centralized email dispatcher that:
    1. Records/updates an EmailLog entry.
    2. Sends email via the chosen sender (Email 1 vs Email 2).
    3. Handles attachments (uploaded files or in-memory content).
    4. Updates EmailLog with delivery status, timestamp, or full error trace.
    Returns: (bool success, EmailLog log_instance)
    """
    if not from_email:
        from_email = get_sender_from_email(sender_choice)

    # Normalize recipient list
    if isinstance(to_email, (list, tuple)):
        recipient_list = list(to_email)
        primary_recipient = recipient_list[0] if recipient_list else ''
    else:
        primary_recipient = str(to_email).strip()
        recipient_list = [primary_recipient]

    # Create or update EmailLog
    if existing_log:
        email_log = existing_log
        email_log.sender_choice = sender_choice
        email_log.from_email = from_email
        email_log.to_email = primary_recipient
        email_log.recipient_name = recipient_name or email_log.recipient_name
        email_log.subject = subject
        email_log.body_text = body_text
        email_log.body_html = body_html or ''
        email_log.retry_count += 1
        email_log.status = 'pending'
        email_log.save()
    else:
        email_log = EmailLog.objects.create(
            sender_choice=sender_choice,
            from_email=from_email,
            to_email=primary_recipient,
            recipient_name=recipient_name,
            subject=subject,
            body_text=body_text,
            body_html=body_html or '',
            email_type=email_type,
            status='pending',
        )

    # Handle attached file upload persistence
    if attachment_file and hasattr(attachment_file, 'name'):
        try:
            email_log.attachment = attachment_file
            email_log.attachment_name = attachment_filename or attachment_file.name
            email_log.save(update_fields=['attachment', 'attachment_name'])
        except Exception as e:
            logger.warning(f"Could not save attachment to EmailLog model: {e}")

    try:
        backend = get_email_connection(sender_choice)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=body_text,
            from_email=from_email,
            to=recipient_list,
            connection=backend,
        )

        if body_html:
            msg.attach_alternative(body_html, "text/html")

        # 1. Attach from InMemory or Uploaded File
        if attachment_file:
            try:
                if hasattr(attachment_file, 'read'):
                    attachment_file.seek(0)
                    content = attachment_file.read()
                    fname = attachment_filename or getattr(attachment_file, 'name', 'attachment')
                else:
                    # File path on disk
                    with open(attachment_file, 'rb') as f:
                        content = f.read()
                    fname = attachment_filename or os.path.basename(attachment_file)

                ctype = attachment_content_type or mimetypes.guess_type(fname)[0] or 'application/octet-stream'
                msg.attach(fname, content, ctype)
            except Exception as e:
                logger.warning(f"Failed attaching uploaded file: {e}")

        # 2. Attach from direct memory/string (e.g. .ics iCalendar file)
        elif attachment_content:
            fname = attachment_filename or 'attachment.dat'
            ctype = attachment_content_type or mimetypes.guess_type(fname)[0] or 'application/octet-stream'
            msg.attach(fname, attachment_content, ctype)

        # 3. Attach from saved EmailLog file on disk (resend scenario)
        elif email_log.attachment and os.path.exists(email_log.attachment.path):
            try:
                with open(email_log.attachment.path, 'rb') as f:
                    content = f.read()
                fname = email_log.attachment_name or os.path.basename(email_log.attachment.name)
                ctype = mimetypes.guess_type(fname)[0] or 'application/octet-stream'
                msg.attach(fname, content, ctype)
            except Exception as e:
                logger.warning(f"Failed attaching persisted file on resend: {e}")

        # Send via connection with automatic dual-port fallback (465 SSL <-> 587 TLS)
        # AND automatic cPanel failover if server firewall blocks Google SMTP (Errno 111)
        try:
            msg.send(fail_silently=False)
        except Exception as first_err:
            err_str = str(first_err)
            if any(k in err_str.lower() for k in ['refused', '111', '110', '10061', 'timeout', 'timed out', 'connecterror', 'errno', 'network', 'ssl', 'reset', 'handshake']):
                current_port = getattr(backend, 'port', 465)
                fallback_port = 587 if current_port == 465 else 465
                fallback_ssl = (fallback_port == 465)
                fallback_tls = not fallback_ssl
                logger.warning(
                    f"Primary SMTP port {current_port} failed ({first_err}). "
                    f"Retrying email dispatch on fallback port {fallback_port} (SSL={fallback_ssl})..."
                )
                try:
                    fallback_backend = get_email_connection(
                        sender_choice,
                        port_override=fallback_port,
                        ssl_override=fallback_ssl,
                        tls_override=fallback_tls,
                    )
                    msg.connection = fallback_backend
                    msg.send(fail_silently=False)
                except Exception as retry_err:
                    # If Email 2 is blocked by server firewall (e.g. [Errno 111] Connection refused),
                    # automatically fail over to Email 1 (cPanel) which is whitelisted on this host!
                    if sender_choice == 'email2':
                        logger.warning(
                            f"Email 2 (Google SMTP) blocked by server firewall ({retry_err}). "
                            "Failing over to Email 1 (mail.uniquetechcamp.org) with Reply-To set to UniqueTechCamp@gmail.com..."
                        )
                        email1_backend = get_email_connection('email1')
                        msg.connection = email1_backend
                        msg.from_email = get_sender_from_email('email1')
                        msg.reply_to = [getattr(settings, 'EMAIL2_HOST_USER', 'UniqueTechCamp@gmail.com')]
                        msg.send(fail_silently=False)
                        email_log.error_message = (
                            f"Dispatched via Email 1 failover (Server firewall blocked outbound Google SMTP: {retry_err}). "
                            "Reply-To set to UniqueTechCamp@gmail.com."
                        )
                    else:
                        raise retry_err
            else:
                raise first_err

        # Update log on success
        email_log.status = 'sent'
        email_log.sent_at = timezone.now()
        email_log.error_message = ''
        email_log.save(update_fields=['status', 'sent_at', 'error_message'])
        logger.info(f"Email successfully sent to {primary_recipient} via [{sender_choice}]")
        return True, email_log

    except Exception as e:
        err_msg = str(e)
        logger.error(f"Failed to send email to {primary_recipient} via [{sender_choice}]: {err_msg}")
        email_log.status = 'failed'
        email_log.error_message = err_msg
        email_log.save(update_fields=['status', 'error_message'])
        return False, email_log
