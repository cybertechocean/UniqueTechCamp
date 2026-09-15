import uuid
from django.db import models
from django.utils import timezone
from services.models import Service

def generate_booking_reference():
    """Generate an elegant, unique booking reference code e.g. UTC-APT-A9B2C4"""
    return f"UTC-APT-{uuid.uuid4().hex[:6].upper()}"

class Appointment(models.Model):
    """
    Model representing a consultation / discovery session booked by a client.
    Can be associated with a specific Service or booked as a general architecture consultation.
    """
    TIME_SLOT_CHOICES = [
        ('09:00 - 10:00', '09:00 AM - 10:00 AM (EAT / UTC+3)'),
        ('10:30 - 11:30', '10:30 AM - 11:30 AM (EAT / UTC+3)'),
        ('12:00 - 13:00', '12:00 PM - 01:00 PM (EAT / UTC+3)'),
        ('14:00 - 15:00', '02:00 PM - 03:00 PM (EAT / UTC+3)'),
        ('15:30 - 16:30', '03:30 PM - 04:30 PM (EAT / UTC+3)'),
        ('17:00 - 18:00', '05:00 PM - 06:00 PM (EAT / UTC+3)'),
    ]

    MEETING_TYPE_CHOICES = [
        ('google_meet', 'Google Meet (Recommended Video Call)'),
        ('whatsapp_call', 'WhatsApp Video / Audio Call'),
        ('phone', 'Direct Phone Call'),
        ('office', 'In-Person at Nairobi CBD Office (Kenya)'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review & Confirmation'),
        ('confirmed', 'Confirmed & Scheduled'),
        ('completed', 'Session Completed'),
        ('rescheduled', 'Rescheduled'),
        ('cancelled', 'Cancelled'),
    ]

    booking_reference = models.CharField(
        max_length=20,
        unique=True,
        default=generate_booking_reference,
        editable=False,
        help_text="Unique reference code for client tracking & calendar sync"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointments',
        help_text="The specific digital solution requested, or empty for general consultation"
    )
    full_name = models.CharField(max_length=150, help_text="Client's full name")
    email = models.EmailField(help_text="Official email address for calendar invite & confirmation")
    phone = models.CharField(max_length=40, help_text="Direct phone or WhatsApp number with country code")
    company_name = models.CharField(max_length=150, blank=True, help_text="Company, startup, or organization name (optional)")
    preferred_date = models.DateField(help_text="Requested date for the consultation session")
    preferred_time_slot = models.CharField(
        max_length=50,
        choices=TIME_SLOT_CHOICES,
        default='10:30 - 11:30',
        help_text="Preferred 1-hour consultation window"
    )
    meeting_type = models.CharField(
        max_length=30,
        choices=MEETING_TYPE_CHOICES,
        default='google_meet',
        help_text="Preferred platform for the consultation"
    )
    project_description = models.TextField(
        help_text="Summary of business goals, technical requirements, or specific challenges"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current booking workflow status"
    )
    meeting_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Google Meet or conference link assigned by UniqueTechCamp"
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes from the engineering & solutions architecture team"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-preferred_date', '-created_at']
        verbose_name = 'Consultation Appointment'
        verbose_name_plural = 'Consultation Appointments'

    def __str__(self):
        service_label = self.service.title if self.service else "General Tech Consultation"
        return f"[{self.booking_reference}] {self.full_name} - {service_label} ({self.preferred_date})"

    @property
    def service_name(self):
        """Helper to return the title of the associated service or generic consultation."""
        if self.service:
            return self.service.title
        return "Custom Digital Architecture & Strategy Consultation"

    @property
    def meeting_type_display_name(self):
        """Friendly label for meeting channel."""
        return dict(self.MEETING_TYPE_CHOICES).get(self.meeting_type, self.meeting_type)

    @property
    def status_display_name(self):
        """Friendly status title."""
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
