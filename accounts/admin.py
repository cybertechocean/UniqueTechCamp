from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = (
        'user',
        'phone_number',
        'company_name',
        'is_email_verified',
        'welcome_email_sent',
        'created_at',
    )
    list_filter = ('is_email_verified', 'welcome_email_sent', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number', 'company_name')
    readonly_fields = ('created_at', 'updated_at', 'email_verification_token', 'email_verification_sent_at')
