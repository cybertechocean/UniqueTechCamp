from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import BulkCampaign, CampaignRecipient, EmailLog

class CampaignRecipientInline(TabularInline):
    model = CampaignRecipient
    extra = 0
    fields = ('name', 'email', 'subject', 'status_badge', 'sent_at', 'error_message')
    readonly_fields = ('name', 'email', 'subject', 'status_badge', 'sent_at', 'error_message')
    can_delete = False

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'sent': '#22c55e',
            'failed': '#ef4444',
        }
        color = colors.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; border-radius: 9999px; background-color: {}20; color: {}; font-size: 11px; font-weight: 700; border: 1px solid {}40;">{}</span>',
            color, color, color, obj.get_status_display()
        )
    status_badge.short_description = "Status"


@admin.register(BulkCampaign)
class BulkCampaignAdmin(ModelAdmin):
    list_display = (
        'campaign_id_display',
        'title',
        'sender_choice_badge',
        'total_recipients',
        'sent_count',
        'failed_count',
        'progress_bar',
        'delay_seconds',
        'status_badge',
        'created_at',
    )
    list_display_links = ('campaign_id_display', 'title')
    list_filter = ('status', 'sender_choice', 'created_at')
    search_fields = ('campaign_id', 'title', 'sender_name', 'sender_email')
    ordering = ('-created_at',)
    readonly_fields = ('campaign_id', 'total_recipients', 'sent_count', 'failed_count', 'created_at', 'completed_at')
    inlines = [CampaignRecipientInline]

    fieldsets = (
        ("Campaign Overview", {
            "fields": ("campaign_id", "title", "status", "created_at", "completed_at")
        }),
        ("Dispatch Configuration & Anti-Spam", {
            "description": "Sender headers and delay interval to protect SMTP reputation.",
            "fields": ("sender_choice", "sender_name", "sender_email", "default_subject", "delay_seconds")
        }),
        ("Uploaded File & Metrics", {
            "fields": ("spreadsheet_file", "total_recipients", "sent_count", "failed_count")
        }),
    )

    def sender_choice_badge(self, obj):
        color = '#22c55e' if obj.sender_choice == 'email1' else '#38bdf8'
        label = "Email 1 (info@)" if obj.sender_choice == 'email1' else "Email 2 (Gmail)"
        return format_html(
            '<span style="font-family: monospace; font-size: 10px; font-weight: 700; color: {}; border: 1px solid {}40; padding: 2px 6px; border-radius: 6px; background-color: {}15;">{}</span>',
            color, color, color, label
        )
    sender_choice_badge.short_description = "Sender"

    def campaign_id_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; font-weight: 700; color: #22c55e;">{}</span>',
            obj.campaign_id
        )
    campaign_id_display.short_description = "Campaign ID"

    def status_badge(self, obj):
        colors = {
            'draft': '#94a3b8',
            'sending': '#38bdf8',
            'completed': '#22c55e',
            'failed': '#ef4444',
        }
        color = colors.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="display: inline-block; padding: 3px 10px; border-radius: 9999px; background-color: {}25; color: {}; font-size: 11px; font-weight: 800; border: 1px solid {}50;">{}</span>',
            color, color, color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def progress_bar(self, obj):
        pct = obj.progress_percentage
        bar_color = '#22c55e' if obj.status == 'completed' else '#38bdf8'
        return format_html(
            '<div style="width: 110px; background-color: #334155; border-radius: 6px; height: 12px; overflow: hidden; display: flex; align-items: center;">'
            '<div style="width: {}%; background-color: {}; height: 100%;"></div>'
            '</div>'
            '<span style="font-size: 11px; font-weight: 700; color: #94a3b8; margin-left: 4px;">{}%</span>',
            pct, bar_color, pct
        )
    progress_bar.short_description = "Delivery Progress"


@admin.register(CampaignRecipient)
class CampaignRecipientAdmin(ModelAdmin):
    list_display = ('name', 'email', 'campaign', 'subject', 'status', 'sent_at')
    list_filter = ('status', 'campaign')
    search_fields = ('name', 'email', 'subject', 'personalized_message')
    readonly_fields = ('sent_at',)


@admin.register(EmailLog)
class EmailLogAdmin(ModelAdmin):
    list_display = (
        'status_badge',
        'sender_badge',
        'to_email',
        'recipient_name',
        'subject',
        'email_type_badge',
        'has_attachment_display',
        'retry_count',
        'created_at',
    )
    list_display_links = ('to_email', 'subject')
    list_filter = ('status', 'sender_choice', 'email_type', 'created_at')
    search_fields = ('to_email', 'recipient_name', 'subject', 'body_text', 'error_message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'sent_at', 'retry_count')

    fieldsets = (
        ("Delivery Status & Sender", {
            "fields": ("status", "sender_choice", "from_email", "to_email", "recipient_name", "created_at", "sent_at", "retry_count")
        }),
        ("Message Content", {
            "fields": ("subject", "email_type", "body_text", "body_html")
        }),
        ("Attachment & Error Info", {
            "fields": ("attachment", "attachment_name", "error_message")
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'sent': '#22c55e',
            'failed': '#ef4444',
        }
        color = colors.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="display: inline-block; padding: 2px 9px; border-radius: 9999px; background-color: {}20; color: {}; font-size: 11px; font-weight: 800; border: 1px solid {}40;">{}</span>',
            color, color, color, obj.get_status_display()
        )
    status_badge.short_description = "Status"

    def sender_badge(self, obj):
        color = '#22c55e' if obj.sender_choice == 'email1' else '#38bdf8'
        label = "Email 1 (info@)" if obj.sender_choice == 'email1' else "Email 2 (Gmail)"
        return format_html(
            '<span style="font-family: monospace; font-size: 10px; font-weight: 700; color: {}; border: 1px solid {}40; padding: 2px 6px; border-radius: 6px; background-color: {}15;">{}</span>',
            color, color, color, label
        )
    sender_badge.short_description = "Sender"

    def email_type_badge(self, obj):
        return format_html(
            '<span style="font-size: 10px; font-weight: 600; text-transform: uppercase; color: #cbd5e1; background-color: #334155; padding: 2px 6px; border-radius: 4px;">{}</span>',
            obj.get_email_type_display()
        )
    email_type_badge.short_description = "Type"

    def has_attachment_display(self, obj):
        if obj.attachment:
            return format_html('<span style="color: #f59e0b; font-weight: 700;">📎 Yes</span>')
        return format_html('<span style="color: #64748b;">No</span>')
    has_attachment_display.short_description = "Attachment"

