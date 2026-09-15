from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Testimonial, FAQ, ContactMessage

@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ('image_thumbnail', 'client_name', 'company', 'rating', 'created_at')
    list_display_links = ('image_thumbnail', 'client_name')
    search_fields = ('client_name', 'company', 'content')
    list_filter = ('rating', 'created_at')

    fieldsets = (
        ("Client Details", {
            "fields": ("client_name", "company", "rating", "content")
        }),
        ("Client Photo / Avatar", {
            "description": "Upload a client photo OR paste an external image URL. Uploaded file takes precedence.",
            "fields": ("image", "image_url")
        }),
    )

    def image_thumbnail(self, obj):
        url = obj.get_image_url
        if url:
            return format_html(
                '<img src="{}" style="width: 36px; height: 36px; object-fit: cover; border-radius: 50%; border: 1px solid #e2e8f0;" loading="lazy" />',
                url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No Avatar</span>')
    image_thumbnail.short_description = "Avatar"

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
