from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import BlogCategory, Post

@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order', 'name')

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('image_thumbnail', 'title', 'category', 'author_name', 'is_published', 'is_featured', 'views_count', 'published_at')
    list_display_links = ('image_thumbnail', 'title')
    list_filter = ('is_published', 'is_featured', 'category')
    search_fields = ('title', 'excerpt', 'tags', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

    fieldsets = (
        ("Article Core", {
            "fields": ("title", "slug", "category", "author_name", "author_role", "read_time", "is_published", "is_featured")
        }),
        ("Featured Visuals", {
            "description": "Upload a cover image OR paste an external image URL (e.g. Unsplash, CDN). Uploaded file takes precedence.",
            "fields": ("featured_image", "image_url")
        }),
        ("Content & Metadata", {
            "fields": ("excerpt", "content", "tags")
        }),
    )

    def image_thumbnail(self, obj):
        url = obj.get_image_url
        if url:
            return format_html(
                '<img src="{}" style="width: 52px; height: 36px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0;" loading="lazy" />',
                url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No Cover</span>')
    image_thumbnail.short_description = "Cover"

