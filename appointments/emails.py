import logging
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def generate_ics_content(appointment):
    """
    Generate an RFC 5545 compliant iCalendar (.ics) file string.
    Enables automatic 1-click addition to Google Calendar, Apple Calendar, and Outlook.
    """
    # Parse slot for start & end time
    time_slot = appointment.preferred_time_slot
    try:
        start_str, end_str = [t.strip() for t in time_slot.split('-')]
        start_h, start_m = [int(x) for x in start_str.split(':')]
        end_h, end_m = [int(x) for x in end_str.split(':')]
    except Exception:
        start_h, start_m = (10, 30)
        end_h, end_m = (11, 30)

    # Convert preferred date to UTC datetime (Nairobi is UTC+3)
    # 10:30 EAT = 07:30 UTC
    dt_start = datetime.datetime.combine(
        appointment.preferred_date,
        datetime.time(start_h, start_m)
    ) - datetime.timedelta(hours=3)

    dt_end = datetime.datetime.combine(
        appointment.preferred_date,
        datetime.time(end_h, end_m)
    ) - datetime.timedelta(hours=3)

    dt_stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    start_fmt = dt_start.strftime("%Y%m%dT%H%M%SZ")
    end_fmt = dt_end.strftime("%Y%m%dT%H%M%SZ")

    service_title = appointment.service.title if appointment.service else "Digital Growth Consultation"
    summary = f"UniqueTechCamp Consultation: {service_title}"
    description = (
        f"UniqueTechCamp Technical Consultation Session\\n\\n"
        f"Booking Reference: {appointment.booking_reference}\\n"
        f"Client: {appointment.full_name}\\n"
        f"Channel: {appointment.meeting_type_display_name}\\n"
        f"Service: {service_title}\\n\\n"
        f"Need assistance or need to reschedule? Contact us on WhatsApp: +254 715 479 955 or email info@uniquetechcamp.org"
    )
    location = "Google Meet / Remote (Details shared via email)" if appointment.meeting_type != 'office' else "UniqueTechCamp HQ, CBD, Nairobi, Kenya"

    ics_content = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//UniqueTechCamp//Consultation Scheduling System//EN\r\n"
        "CALSCALE:GREGORIAN\r\n"
        "METHOD:REQUEST\r\n"
        "BEGIN:VEVENT\r\n"
        f"UID:{appointment.booking_reference}@uniquetechcamp.org\r\n"
        f"DTSTAMP:{dt_stamp}\r\n"
        f"DTSTART:{start_fmt}\r\n"
        f"DTEND:{end_fmt}\r\n"
        f"SUMMARY:{summary}\r\n"
        f"DESCRIPTION:{description}\r\n"
        f"LOCATION:{location}\r\n"
        "STATUS:CONFIRMED\r\n"
        "SEQUENCE:0\r\n"
        "BEGIN:VALARM\r\n"
        "TRIGGER:-PT30M\r\n"
        "ACTION:DISPLAY\r\n"
        "DESCRIPTION:Consultation Session with UniqueTechCamp in 30 minutes\r\n"
        "END:VALARM\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    return ics_content


def send_appointment_emails(appointment, request=None):
    """
    Robust dual-dispatch email routine:
    1. Send Client Confirmation Email with HTML layout + attached .ics calendar invite.
    2. Send Admin Notification Email to solutions architecture team.
    Catches all network / SMTP errors cleanly without disrupting user flow.
    """
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'UniqueTechCamp Web Developers <info@uniquetechcamp.org>')
    admin_recipients = [
        getattr(settings, 'ADMIN_EMAIL_PRIMARY', 'info@uniquetechcamp.org'),
        getattr(settings, 'ADMIN_EMAIL_GMAIL', 'UniqueTechCamp@gmail.com'),
    ]

    ics_data = generate_ics_content(appointment)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. CLIENT CONFIRMATION EMAIL
    # ──────────────────────────────────────────────────────────────────────────
    try:
        client_subject = f"Appointment Confirmed [{appointment.booking_reference}]: {appointment.service_name} - UniqueTechCamp"
        client_context = {
            'appointment': appointment,
            'whatsapp_phone': '254715479955',
            'support_email': 'info@uniquetechcamp.org',
            'website_url': 'https://uniquetechcamp.org',
        }
        client_html = render_to_string('emails/appointment_confirmation.html', client_context)
        client_text = strip_tags(client_html)

        from marketing.email_service import send_robust_email
        send_robust_email(
            to_email=appointment.email,
            subject=client_subject,
            body_text=client_text,
            body_html=client_html,
            sender_choice='email1',
            recipient_name=appointment.full_name,
            attachment_content=ics_data,
            attachment_filename=f"UniqueTechCamp-Consultation-{appointment.booking_reference}.ics",
            attachment_content_type="text/calendar; method=REQUEST; charset=UTF-8",
            email_type='appointment',
        )
        logger.info(f"Client consultation confirmation email dispatched for {appointment.booking_reference}")
    except Exception as e:
        logger.error(f"Error dispatching client appointment email ({appointment.booking_reference}): {e}")

    # ──────────────────────────────────────────────────────────────────────────
    # 2. ADMIN ALERT EMAIL
    # ──────────────────────────────────────────────────────────────────────────
    try:
        admin_subject = f"[New Consultation] {appointment.full_name} - {appointment.service_name} ({appointment.preferred_date})"
        admin_context = {
            'appointment': appointment,
            'whatsapp_link': f"https://wa.me/{appointment.phone.replace('+', '').replace(' ', '')}?text=Hello%20{appointment.full_name},%20this%20is%20UniqueTechCamp%20regarding%20your%20scheduled%20consultation%20({appointment.booking_reference}).",
            'admin_url': f"https://uniquetechcamp.org/admin/appointments/appointment/{appointment.id}/change/"
        }
        admin_html = render_to_string('emails/appointment_admin_alert.html', admin_context)
        admin_text = strip_tags(admin_html)

        from marketing.email_service import send_robust_email
        for admin_email in admin_recipients:
            send_robust_email(
                to_email=admin_email,
                subject=admin_subject,
                body_text=admin_text,
                body_html=admin_html,
                sender_choice='email1',
                recipient_name='UniqueTechCamp Admin',
                attachment_content=ics_data,
                attachment_filename=f"Consultation-{appointment.booking_reference}.ics",
                attachment_content_type="text/calendar; method=REQUEST; charset=UTF-8",
                email_type='appointment',
            )
        logger.info(f"Admin consultation alert email dispatched for {appointment.booking_reference}")
    except Exception as e:
        logger.error(f"Error dispatching admin consultation alert ({appointment.booking_reference}): {e}")

