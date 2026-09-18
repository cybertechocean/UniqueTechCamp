from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = (
        'booking_reference_display',
        'full_name',
        'service_display',
        'preferred_date',
        'preferred_time_slot',
        'source_badge',
        'channel_badge',
        'status_badge',
        'client_contact_links',
    )
    list_display_links = ('booking_reference_display', 'full_name')
    list_filter = ('source', 'status', 'meeting_type', 'preferred_date', 'created_at')
    search_fields = ('booking_reference', 'full_name', 'email', 'phone', 'company_name', 'project_description')
    date_hierarchy = 'preferred_date'
    ordering = ('-preferred_date', '-created_at')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')

    fieldsets = (
        ("Booking Reference & Origin", {
            "fields": ("booking_reference", "status", "source", "created_at", "updated_at")
        }),
        ("Client Information", {
            "fields": ("full_name", "email", "phone", "company_name")
        }),
        ("Session Logistics & Platform", {
            "fields": ("service", "preferred_date", "preferred_time_slot", "meeting_type", "meeting_link")
        }),
        ("Requirements & Project Scope", {
            "fields": ("project_description",)
        }),
        ("Internal Architecture Notes", {
            "description": "Internal team notes, discovery findings, and proposal milestones.",
            "fields": ("admin_notes",)
        }),
    )

    def booking_reference_display(self, obj):
        return format_html(
            '<span style="font-family: monospace; font-weight: 700; color: #22c55e;">{}</span>',
            obj.booking_reference
        )
    booking_reference_display.short_description = "Ref Code"

    def service_display(self, obj):
        if obj.service:
            return format_html(
                '<span style="font-weight: 600; color: #38bdf8;">{}</span>',
                obj.service.title
            )
        return format_html('<span style="color: #94a3b8; font-style: italic;">General Consultation</span>')
    service_display.short_description = "Service"

    def source_badge(self, obj):
        if obj.source == 'ai_assistant':
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 9999px; background-color: rgba(16, 185, 129, 0.2); color: #34d399; font-size: 11px; font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.4);">'
                '🤖 AI Assistant</span>'
            )
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; border-radius: 9999px; background-color: rgba(148, 163, 184, 0.15); color: #94a3b8; font-size: 11px; font-weight: 600; border: 1px solid rgba(148, 163, 184, 0.25);">'
            '🌐 Web Form</span>'
        )
    source_badge.short_description = "Origin"

    def channel_badge(self, obj):
        colors = {
            'google_meet': '#0284c7',
            'whatsapp_call': '#16a34a',
            'phone': '#eab308',
            'office': '#8b5cf6',
        }
        color = colors.get(obj.meeting_type, '#64748b')
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; border-radius: 9999px; background-color: {}20; color: {}; font-size: 11px; font-weight: 700; border: 1px solid {}40;">{}</span>',
            color, color, color, obj.meeting_type_display_name
        )
    channel_badge.short_description = "Channel"

    def status_badge(self, obj):
        badges = {
            'pending': ('#f59e0b', 'Pending'),
            'confirmed': ('#22c55e', 'Confirmed'),
            'completed': ('#3b82f6', 'Completed'),
            'rescheduled': ('#ec4899', 'Rescheduled'),
            'cancelled': ('#ef4444', 'Cancelled'),
        }
        color, label = badges.get(obj.status, ('#94a3b8', obj.status))
        return format_html(
            '<span style="display: inline-block; padding: 3px 10px; border-radius: 9999px; background-color: {}25; color: {}; font-size: 11px; font-weight: 800; border: 1px solid {}50;">{}</span>',
            color, color, color, label
        )
    status_badge.short_description = "Status"

    def client_contact_links(self, obj):
        wa_digits = ''.join(c for c in obj.phone if c.isdigit())
        return format_html(
            '<div style="display: flex; gap: 8px;">'
            '<a href="https://wa.me/{}" target="_blank" style="color: #22c55e; font-size: 12px; font-weight: 700; text-decoration: none;">WhatsApp</a>'
            '<span style="color: #64748b;">|</span>'
            '<a href="mailto:{}" style="color: #38bdf8; font-size: 12px; font-weight: 700; text-decoration: none;">Email</a>'
            '</div>',
            wa_digits, obj.email
        )
    client_contact_links.short_description = "Contact Direct"
