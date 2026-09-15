from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import Service, ServiceCategory, ServiceFeature, ServiceFAQ, ServiceImage

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(ModelAdmin):
    list_display = ('name', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ServiceImageInline(TabularInline):
    model = ServiceImage
    extra = 1
    fields = ('image_preview', 'image', 'image_url', 'caption', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        url = obj.get_image_url if obj else None
        if url:
            return format_html(
                '<img src="{}" style="width: 72px; height: 48px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" />',
                url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No Image</span>')
    image_preview.short_description = "Preview"

class ServiceFeatureInline(TabularInline):
    model = ServiceFeature
    extra = 1

class ServiceFAQInline(TabularInline):
    model = ServiceFAQ
    extra = 1

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ('image_thumbnail', 'title', 'category', 'icon_name', 'order', 'is_featured', 'is_active')
    list_display_links = ('image_thumbnail', 'title')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('title', 'short_description', 'category__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_featured', 'is_active')
    inlines = [ServiceImageInline, ServiceFeatureInline, ServiceFAQInline]
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "category", "icon_name", "order", "is_featured", "is_active")
        }),
        ("Featured Visuals", {
            "description": "Upload a local image file OR paste an external image URL. Uploaded file takes precedence.",
            "fields": ("featured_image", "image_url")
        }),
        ("Service Details", {
            "fields": ("short_description", "overview", "benefits", "process")
        }),
    )

    def image_thumbnail(self, obj):
        url = obj.get_image_url
        if url:
            return format_html(
                '<img src="{}" style="width: 48px; height: 36px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" />',
                url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No Image</span>')
    image_thumbnail.short_description = "Cover"
