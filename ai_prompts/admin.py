from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PromptCategory, AIPrompt, PromptAssistanceRequest


@admin.register(PromptCategory)
class PromptCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('order', 'name')


@admin.register(AIPrompt)
class AIPromptAdmin(ModelAdmin):
    list_display = (
        'title',
        'category',
        'is_free',
        'price_kes',
        'price_usd',
        'difficulty_level',
        'copy_count',
        'view_count',
        'is_featured',
        'is_published',
    )
    list_filter = ('is_free', 'is_featured', 'is_published', 'difficulty_level', 'category')
    search_fields = ('title', 'tagline', 'overview', 'master_prompt', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('copy_count', 'download_count', 'view_count', 'created_at', 'updated_at')


@admin.register(PromptAssistanceRequest)
class PromptAssistanceRequestAdmin(ModelAdmin):
    list_display = (
        'client_name',
        'prompt',
        'client_phone',
        'client_email',
        'status',
        'mpesa_reference',
        'amount_paid',
        'created_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('client_name', 'client_email', 'client_phone', 'mpesa_reference', 'requirements')
