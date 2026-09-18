import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.contrib import messages
from unfold.admin import ModelAdmin, TabularInline
from .models import LeadCapture, ChatSession, ChatMessage
from .emails import send_lead_transcript_email


class ChatMessageInline(TabularInline):
    model = ChatMessage
    extra = 0
    fields = ('sender', 'message', 'model_used', 'is_fallback', 'action_type', 'created_at')
    readonly_fields = ('sender', 'message', 'model_used', 'is_fallback', 'action_type', 'created_at')
    can_delete = False


@admin.register(LeadCapture)
class LeadCaptureAdmin(ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'whatsapp_link',
        'industry',
        'associated_appointment_badge',
        'transcript_badge',
        'admin_alert_badge',
        'created_at',
    )
    list_filter = ('transcript_sent', 'admin_alert_sent', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'industry', 'business_bottleneck', 'qualification_notes')
    readonly_fields = ('created_at', 'updated_at', 'transcript_sent_at', 'admin_alert_sent_at')
    actions = ['export_as_csv', 'resend_transcript_action']

    def whatsapp_link(self, obj):
        digits = obj.clean_whatsapp_digits
        return format_html(
            '<a href="https://wa.me/{}" target="_blank" style="color: #22c55e; font-weight: 700; text-decoration: none;">'
            '<i class="fa-brands fa-whatsapp"></i> {}</a>',
            digits, obj.phone
        )
    whatsapp_link.short_description = "WhatsApp Phone"

    def associated_appointment_badge(self, obj):
        if obj.associated_appointment:
            apt = obj.associated_appointment
            return format_html(
                '<a href="/admin/appointments/appointment/{}/change/" style="display: inline-block; padding: 2px 8px; border-radius: 9999px; background-color: rgba(34, 197, 94, 0.2); color: #22c55e; font-weight: 700; font-size: 11px; text-decoration: none; border: 1px solid rgba(34, 197, 94, 0.4);">'
                '📅 {}</a>',
                apt.id, apt.booking_reference
            )
        return format_html('<span style="color: #64748b; font-size: 11px;">Not Scheduled</span>')
    associated_appointment_badge.short_description = "Consultation"

    def transcript_badge(self, obj):
        if obj.transcript_sent:
            return format_html(
                '<span style="padding: 2px 8px; border-radius: 9999px; background-color: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: 700; font-size: 11px;">Sent</span>'
            )
        return format_html(
            '<span style="padding: 2px 8px; border-radius: 9999px; background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; font-weight: 700; font-size: 11px;">Pending</span>'
        )
    transcript_badge.short_description = "Transcript"

    def admin_alert_badge(self, obj):
        if obj.admin_alert_sent:
            return format_html(
                '<span style="padding: 2px 8px; border-radius: 9999px; background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; font-weight: 700; font-size: 11px;">Dispatched</span>'
            )
        return format_html(
            '<span style="padding: 2px 8px; border-radius: 9999px; background-color: rgba(239, 68, 68, 0.2); color: #f87171; font-weight: 700; font-size: 11px;">Not Sent</span>'
        )
    admin_alert_badge.short_description = "Admin Alert"

    @admin.action(description="Export Selected Leads as CSV")
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="UniqueTechCamp-AI-Leads.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Full Name', 'Email', 'Phone', 'Industry', 'Bottleneck / Challenge',
            'Timeline', 'Budget/Scope', 'Transcript Sent', 'Booked Reference', 'Created At'
        ])
        for lead in queryset:
            apt_ref = lead.associated_appointment.booking_reference if lead.associated_appointment else ''
            writer.writerow([
                lead.full_name, lead.email, lead.phone, lead.industry, lead.business_bottleneck,
                lead.preferred_timeline, lead.budget_or_scope, lead.transcript_sent, apt_ref, lead.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        return response

    @admin.action(description="Resend AI Consultation Transcript to Client")
    def resend_transcript_action(self, request, queryset):
        sent_count = 0
        for lead in queryset:
            session = lead.chat_sessions.order_by('-created_at').first()
            if session and send_lead_transcript_email(lead, session, request):
                sent_count += 1
        messages.success(request, f"Transcript emails successfully dispatched to {sent_count} client(s).")


@admin.register(ChatSession)
class ChatSessionAdmin(ModelAdmin):
    list_display = (
        'session_id_display',
        'lead_display',
        'status_badge',
        'message_count_display',
        'ip_address',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'is_active', 'created_at')
    search_fields = ('session_id', 'lead__full_name', 'lead__email', 'lead__phone', 'ip_address')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    inlines = [ChatMessageInline]
    actions = ['email_transcript_action']

    def session_id_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; font-weight: 700; color: #38bdf8;">[{}]</span>',
            str(obj.session_id)[:8]
        )
    session_id_display.short_description = "Session ID"

    def lead_display(self, obj):
        if obj.lead:
            return format_html(
                '<a href="/admin/ai_assistant/leadcapture/{}/change/" style="font-weight: 700; color: #22c55e; text-decoration: none;">{}</a>',
                obj.lead.id, obj.lead.full_name
            )
        return format_html('<span style="color: #94a3b8; font-style: italic;">Anonymous Prospect</span>')
    lead_display.short_description = "Lead Profile"

    def status_badge(self, obj):
        colors = {
            'exploring': '#94a3b8',
            'lead_captured': '#38bdf8',
            'booking_initiated': '#f59e0b',
            'appointment_booked': '#22c55e',
            'concluded': '#64748b',
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(
            '<span style="padding: 3px 9px; border-radius: 9999px; background-color: {}20; color: {}; font-weight: 700; font-size: 11px; border: 1px solid {}40;">{}</span>',
            color, color, color, obj.get_status_display()
        )
    status_badge.short_description = "Session Status"

    def message_count_display(self, obj):
        return format_html(
            '<span style="font-weight: 700; color: #f8fafc;">{} turns</span>',
            obj.message_count
        )
    message_count_display.short_description = "Messages"

    @admin.action(description="Email Complete Transcript to Client")
    def email_transcript_action(self, request, queryset):
        success_count = 0
        for session in queryset:
            if session.lead and send_lead_transcript_email(session.lead, session, request):
                success_count += 1
        messages.success(request, f"Transcript successfully emailed for {success_count} session(s).")


@admin.register(ChatMessage)
class ChatMessageAdmin(ModelAdmin):
    list_display = (
        'session_link',
        'sender_badge',
        'message_snippet',
        'model_used_badge',
        'is_fallback_badge',
        'action_type',
        'created_at',
    )
    list_filter = ('sender', 'is_fallback', 'action_type', 'created_at')
    search_fields = ('message', 'session__session_id', 'model_used')
    readonly_fields = ('created_at',)

    def session_link(self, obj):
        return format_html(
            '<a href="/admin/ai_assistant/chatsession/{}/change/" style="font-family: monospace; font-weight: 700; color: #38bdf8;">[{}]</a>',
            obj.session.id, str(obj.session.session_id)[:8]
        )
    session_link.short_description = "Session"

    def sender_badge(self, obj):
        if obj.sender == 'user':
            return format_html('<span style="color: #38bdf8; font-weight: 700;">Client</span>')
        elif obj.sender == 'assistant':
            return format_html('<span style="color: #22c55e; font-weight: 700;">AI Assistant</span>')
        return format_html('<span style="color: #eab308; font-weight: 700;">System</span>')
    sender_badge.short_description = "Sender"

    def message_snippet(self, obj):
        return (obj.message[:80] + '...') if len(obj.message) > 80 else obj.message
    message_snippet.short_description = "Message Content"

    def model_used_badge(self, obj):
        if not obj.model_used:
            return '-'
        return format_html(
            '<span style="font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 6px; background-color: #1e293b; color: #a5b4fc;">{}</span>',
            obj.model_used
        )
    model_used_badge.short_description = "Model Used"

    def is_fallback_badge(self, obj):
        if obj.is_fallback:
            return format_html('<span style="color: #f59e0b; font-weight: 800; font-size: 11px;">⚠️ Fallback</span>')
        return format_html('<span style="color: #22c55e; font-weight: 600; font-size: 11px;">Primary</span>')
    is_fallback_badge.short_description = "Tier Status"
