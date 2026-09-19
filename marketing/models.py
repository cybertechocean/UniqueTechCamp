import uuid
from django.db import models
from django.utils import timezone

def generate_campaign_id():
    """Generate a readable campaign identifier e.g. UTC-MKT-9F2B4D"""
    return f"UTC-MKT-{uuid.uuid4().hex[:6].upper()}"

class BulkCampaign(models.Model):
    """
    Model representing an email marketing or outreach broadcast campaign.
    Supports importing from Excel (.xlsx) or CSV spreadsheets with custom columns.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft / Uploaded'),
        ('sending', 'In Progress / Sending'),
        ('completed', 'Completed Successfully'),
        ('failed', 'Encountered Errors'),
    ]

    campaign_id = models.CharField(
        max_length=25,
        unique=True,
        default=generate_campaign_id,
        editable=False,
        help_text="Unique tracking code for this broadcast"
    )
    title = models.CharField(
        max_length=200,
        help_text="Campaign name e.g. 'October 2026 Tech & AI Outreach'"
    )
    sender_choice = models.CharField(
        max_length=20,
        choices=[
            ('email1', 'Email 1: info@uniquetechcamp.org (Primary)'),
            ('email2', 'Email 2: UniqueTechCamp@gmail.com (Alternative)'),
        ],
        default='email1',
        help_text="Choose which email account to send from"
    )
    sender_name = models.CharField(
        max_length=150,
        default="UniqueTechCamp Solutions",
        help_text="Sender display name shown in recipients' inbox"
    )
    sender_email = models.EmailField(
        default="info@uniquetechcamp.org",
        help_text="From email address"
    )
    default_subject = models.CharField(
        max_length=255,
        blank=True,
        help_text="Fallback subject line if spreadsheet row has no specific subject"
    )
    LAYOUT_CHOICES = [
        ('branded', 'UniqueTechCamp Branded (Top Logo + 9 Social Channels + Support Box)'),
        ('welcome', 'Official High-Converting Welcome Email Layout'),
        ('plain', 'Clean Direct Message (Minimalist Text)'),
    ]
    email_format = models.CharField(
        max_length=20,
        choices=LAYOUT_CHOICES,
        default='branded',
        help_text="Email layout template to wrap broadcast messages"
    )
    spreadsheet_file = models.FileField(
        upload_to='marketing/spreadsheets/',
        help_text="Uploaded Excel (.xlsx) or CSV spreadsheet"
    )
    delay_seconds = models.FloatField(
        default=2.0,
        help_text="Delay between emails in seconds (e.g. 1.0 to 10.0) to comply with SMTP rate limits and avoid spam filters"
    )
    total_recipients = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bulk Email Campaign'
        verbose_name_plural = 'Bulk Email Campaigns'

    def __str__(self):
        return f"[{self.campaign_id}] {self.title} ({self.sent_count}/{self.total_recipients})"

    @property
    def progress_percentage(self):
        """Calculate completion percentage 0-100%."""
        if self.total_recipients == 0:
            return 0
        return int((self.sent_count + self.failed_count) / self.total_recipients * 100)

    @property
    def is_finished(self):
        return self.status in ('completed', 'failed')


class CampaignRecipient(models.Model):
    """
    Individual recipient within an email campaign with custom personalized subject and body.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Dispatch'),
        ('sent', 'Sent Successfully'),
        ('failed', 'Delivery Failed'),
    ]

    campaign = models.ForeignKey(
        BulkCampaign,
        related_name='recipients',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150, blank=True, help_text="Recipient's name or title")
    email = models.EmailField(help_text="Recipient's email address")
    subject = models.CharField(max_length=255, help_text="Personalized subject line")
    personalized_message = models.TextField(help_text="Personalized body or message for this contact")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    error_message = models.TextField(blank=True, help_text="Error trace if delivery failed")
    VERIFICATION_CHOICES = [
        ('unverified', 'Unverified'),
        ('verified', 'Verified Clean'),
        ('risky', 'Risky / Role-Based'),
        ('invalid', 'Invalid / Dead Domain'),
        ('suppressed', 'Suppressed / Bounced'),
    ]
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_CHOICES,
        default='unverified',
        db_index=True,
        help_text="Deliverability score from pre-send verification shield"
    )
    verification_reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Verification check result or reason"
    )
    is_deliverable = models.BooleanField(
        default=True,
        help_text="Whether this contact is safe to send to without risking reputation"
    )
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Campaign Recipient'
        verbose_name_plural = 'Campaign Recipients'

    def __str__(self):
        return f"{self.name or self.email} - {self.status}"


class EmailSuppressionList(models.Model):
    """
    Global suppression list preventing dispatches to emails that hard-bounced (550),
    unsubscribed, or were flagged as spam traps / dead domains.
    Protects sender domain and SMTP account reputation from blacklisting.
    """
    REASON_CHOICES = [
        ('hard_bounce', 'Hard Bounce (550 Mailbox Does Not Exist)'),
        ('invalid_domain', 'Invalid / Dead Domain (No MX Records)'),
        ('spam_trap', 'Spam Trap / Blacklist Hazard'),
        ('disposable', 'Disposable / Temporary Email'),
        ('unsubscribed', 'Recipient Unsubscribed'),
        ('manual_block', 'Manually Blocked by Admin'),
    ]

    email = models.EmailField(unique=True, db_index=True, help_text="Suppressed email address")
    reason = models.CharField(
        max_length=30,
        choices=REASON_CHOICES,
        default='hard_bounce',
        help_text="Reason for suppression"
    )
    detail = models.TextField(blank=True, help_text="Error message or source of suppression")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Suppressed Email'
        verbose_name_plural = 'Suppression List'

    def __str__(self):
        return f"[{self.get_reason_display()}] {self.email}"


class EmailLog(models.Model):
    """
    Comprehensive persistent log of all single, system, and marketing email dispatches.
    Allows viewing, editing, and 1-click resending of failed emails.
    """
    SENDER_CHOICES = [
        ('email1', 'Email 1: info@uniquetechcamp.org (Primary)'),
        ('email2', 'Email 2: UniqueTechCamp@gmail.com (Alternative - Google App Password)'),
    ]
    EMAIL_TYPE_CHOICES = [
        ('single', 'Single / Custom Email'),
        ('welcome', 'Welcome Email'),
        ('campaign', 'Marketing Campaign'),
        ('appointment', 'Appointment Booking'),
        ('contact', 'Contact Form Autoresponder'),
        ('system', 'System Notification'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Dispatch'),
        ('sent', 'Sent Successfully'),
        ('failed', 'Delivery Failed'),
    ]

    sender_choice = models.CharField(
        max_length=20,
        choices=SENDER_CHOICES,
        default='email1',
        help_text="Email account used for sending"
    )
    from_email = models.CharField(max_length=255, help_text="From address header")
    to_email = models.EmailField(help_text="Recipient's email address")
    recipient_name = models.CharField(max_length=150, blank=True, help_text="Recipient's name")
    subject = models.CharField(max_length=255, help_text="Subject line")
    body_text = models.TextField(blank=True, help_text="Plain text email body")
    body_html = models.TextField(blank=True, help_text="HTML formatted email body")

    attachment = models.FileField(
        upload_to='marketing/attachments/%Y/%m/',
        null=True,
        blank=True,
        help_text="Attached file (e.g. PDF, Document, Image)"
    )
    attachment_name = models.CharField(max_length=255, blank=True, help_text="Original attachment filename")

    email_type = models.CharField(
        max_length=30,
        choices=EMAIL_TYPE_CHOICES,
        default='single',
        help_text="Category of this email"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    error_message = models.TextField(blank=True, help_text="Error message if delivery failed")
    retry_count = models.PositiveIntegerField(default=0, help_text="Number of resend attempts")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'

    def __str__(self):
        return f"[{self.get_status_display()}] {self.to_email} - {self.subject[:40]}"

    @property
    def has_attachment(self):
        return bool(self.attachment)
