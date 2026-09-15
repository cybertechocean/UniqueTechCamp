from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import Project, ProjectCategory, ProjectScreenshot

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProjectScreenshotInline(TabularInline):
    model = ProjectScreenshot
    extra = 1
    fields = ('image_preview', 'image', 'image_url', 'caption')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        url = obj.get_image_url if obj else None
        if url:
            return format_html(
                '<img src="{}" style="width: 72px; height: 48px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" loading="lazy" />',
                url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No Image</span>')
    image_preview.short_description = "Preview"

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ('image_thumbnail', 'title', 'category', 'client_name', 'date', 'order')
    list_display_links = ('image_thumbnail', 'title')
    list_filter = ('category', 'date', 'created_at')
    search_fields = ('title', 'client_name', 'technologies', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    date_hierarchy = 'date'
    inlines = [ProjectScreenshotInline]

    fieldsets = (
        ("Project Identification", {
            "fields": ("title", "slug", "category", "client_name", "date", "order", "live_demo_url")
        }),
        ("Featured Visuals", {
            "description": "Upload a local image file OR paste an external image URL (e.g. Unsplash, CDN). Uploaded file takes precedence.",
            "fields": ("featured_image", "image_url")
        }),
        ("Content & Architecture", {
            "fields": ("technologies", "short_description", "description", "case_study", "results_achieved")
        }),
    )

    def image_thumbnail(self, obj):
        url = obj.get_image_url
        if url:
            return format_html(
                '<img src="{}" style="width: 52px; height: 36px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" loading="lazy" />',
                url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No Image</span>')
    image_thumbnail.short_description = "Visual"

