from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import PromptCategory, AIPrompt, PromptAssistanceRequest, PromptPurchase


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


@admin.register(PromptPurchase)
class PromptPurchaseAdmin(ModelAdmin):
    list_display = (
        'client_name',
        'prompt',
        'payment_method',
        'transaction_code',
        'status',
        'is_verified',
        'client_phone',
        'client_email',
        'created_at',
    )
    list_filter = ('is_verified', 'status', 'payment_method', 'created_at')
    search_fields = ('client_name', 'client_email', 'client_phone', 'transaction_code', 'payment_message')
    readonly_fields = ('created_at', 'updated_at', 'verified_at')
    actions = ['verify_and_approve_access', 'mark_rejected']

    def verify_and_approve_access(self, request, queryset):
        import threading
        from django.utils import timezone
        from .emails import send_prompt_access_approved_email

        count = 0
        for purchase in queryset:
            purchase.is_verified = True
            purchase.status = 'approved'
            purchase.verified_at = timezone.now()
            if not purchase.approval_email_sent:
                threading.Thread(
                    target=send_prompt_access_approved_email,
                    args=(purchase,),
                    daemon=True
                ).start()
                purchase.approval_email_sent = True
            purchase.save()
            count += 1

        self.message_user(
            request,
            f"Successfully verified {count} prompt access order(s). Access is unlocked and confirmation email(s) dispatched to clients."
        )

    verify_and_approve_access.short_description = "✅ Verify & Approve Prompt Access (Dispatches Client Email)"

    def mark_rejected(self, request, queryset):
        queryset.update(is_verified=False, status='rejected')
        self.message_user(request, "Selected order(s) marked as rejected.")

    mark_rejected.short_description = "❌ Mark as Rejected"

    def save_model(self, request, obj, form, change):
        import threading
        from django.utils import timezone
        from .emails import send_prompt_access_approved_email

        if obj.is_verified or obj.status == 'approved':
            obj.is_verified = True
            obj.status = 'approved'
            if not obj.verified_at:
                obj.verified_at = timezone.now()

            if not obj.approval_email_sent:
                threading.Thread(
                    target=send_prompt_access_approved_email,
                    args=(obj,),
                    daemon=True
                ).start()
                obj.approval_email_sent = True

        super().save_model(request, obj, form, change)
