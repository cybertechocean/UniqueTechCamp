from django.contrib import admin
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
    list_display = ('title', 'category', 'author_name', 'is_published', 'is_featured', 'views_count', 'published_at')
    list_filter = ('is_published', 'is_featured', 'category')
    search_fields = ('title', 'excerpt', 'tags', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
