import uuid
from django.db import models
from django.conf import settings
from appointments.models import Appointment

class LeadCapture(models.Model):
    """
    Captures verified prospective client leads gathered via the AI Assistant.
    Stores contact information, industry scoping, qualification insights, and notification telemetry.
    """
    full_name = models.CharField(max_length=150, help_text="Prospective client's full name")
    email = models.EmailField(help_text="Verified client email address")
    phone = models.CharField(max_length=50, help_text="WhatsApp or phone number with international country code (e.g. +254...)")
    industry = models.CharField(max_length=120, blank=True, help_text="Client's industry or business niche")
    business_bottleneck = models.TextField(blank=True, help_text="Current bottleneck or business challenge identified")
    preferred_timeline = models.CharField(max_length=100, blank=True, help_text="Desired delivery timeline or target launch date")
    budget_or_scope = models.CharField(max_length=120, blank=True, help_text="Project scale, scope tier, or budget signal")
    qualification_notes = models.TextField(blank=True, help_text="Automated or architectural notes from conversation scoping")
    transcript_sent = models.BooleanField(default=False, help_text="Whether the branded conversation transcript was emailed to client")
    transcript_sent_at = models.DateTimeField(null=True, blank=True)
    admin_alert_sent = models.BooleanField(default=False, help_text="Whether real-time high priority alert was dispatched to admin desk")
    admin_alert_sent_at = models.DateTimeField(null=True, blank=True)
    associated_appointment = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_lead_source',
        help_text="Consultation appointment scheduled during or subsequent to the AI session"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Captured Lead'
        verbose_name_plural = 'AI Captured Leads'

    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.phone}"

    @property
    def clean_whatsapp_digits(self):
        return ''.join(c for c in self.phone if c.isdigit())


class ChatSession(models.Model):
    """
    Tracks an interactive AI assistant conversation session.
    Preserves initial pending queries, associates authenticated users or anonymous leads, and tracks lifecycle state.
    """
    STATUS_CHOICES = [
        ('exploring', 'Initial Exploring'),
        ('lead_captured', 'Lead Captured & Qualified'),
        ('booking_initiated', 'Consultation Booking Initiated'),
        ('appointment_booked', 'Appointment Booked'),
        ('concluded', 'Session Concluded'),
    ]

    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_chat_sessions',
        help_text="Logged in client account if authenticated"
    )
    lead = models.ForeignKey(
        LeadCapture,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chat_sessions',
        help_text="Captured prospect profile linked to this session"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='exploring')
    pending_query = models.TextField(
        blank=True,
        help_text="Client inquiry preserved while contact information is being requested and validated"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'AI Chat Session'
        verbose_name_plural = 'AI Chat Sessions'

    def __str__(self):
        lead_name = self.lead.full_name if self.lead else (self.user.get_full_name() if self.user else "Anonymous Visitor")
        return f"Session [{str(self.session_id)[:8]}] - {lead_name} ({self.get_status_display()})"

    @property
    def message_count(self):
        return self.messages.count()


class ChatMessage(models.Model):
    """
    Represents an individual conversational turn in a session.
    Records sender, message content, Gemini model telemetry, fallback status, and structured interaction cards.
    """
    SENDER_CHOICES = [
        ('user', 'Prospective Client'),
        ('assistant', 'UniqueTechCamp AI Assistant'),
        ('system', 'System / Action Event'),
    ]

    ACTION_TYPE_CHOICES = [
        ('normal', 'Standard Conversational Turn'),
        ('lead_form', 'Interactive Lead Capture Form'),
        ('slot_picker', 'Consultation Time-Slot Discovery Picker'),
        ('booking_card', 'Confirmed Appointment Summary Card'),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    message = models.TextField()
    model_used = models.CharField(
        max_length=100,
        blank=True,
        help_text="Exact Gemini model that fulfilled this turn (e.g. gemini-2.5-flash, gemini-2.0-flash)"
    )
    is_fallback = models.BooleanField(
        default=False,
        help_text="Indicates if this response was generated via a fallback model due to rate limit or quota interception"
    )
    action_type = models.CharField(
        max_length=40,
        choices=ACTION_TYPE_CHOICES,
        default='normal',
        help_text="Type of special interactive card rendered alongside this message"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Structured payloads e.g. slot choices, booking details, lead capture fields, or diagnostic logs"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'AI Chat Message'
        verbose_name_plural = 'AI Chat Messages'

    def __str__(self):
        return f"[{self.session.session_id.hex[:6]}] {self.sender}: {self.message[:40]}"
