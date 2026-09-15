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
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Campaign Recipient'
        verbose_name_plural = 'Campaign Recipients'

    def __str__(self):
        return f"{self.name or self.email} - {self.status}"
