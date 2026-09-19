from django.urls import path
from .views import (
    DownloadTemplateView,
    CampaignDashboardView,
    CampaignDetailView,
    CampaignSendTestView,
    CampaignStartSendingView,
    CampaignResetStatusView,
    CampaignStatusApiView,
    CampaignDispatchStepApiView,
    CampaignValidateContactsView,
    CampaignPruneInvalidView,
    SendSingleEmailView,
    EmailLogListView,
    EmailLogResendView,
    EmailLogEditView,
    EmailLogDeleteView,
    ResendAllFailedEmailsView,
    SyncWelcomeLogsView,
)

app_name = 'marketing'

urlpatterns = [
    path('', CampaignDashboardView.as_view(), name='dashboard'),
    path('template/download/', DownloadTemplateView.as_view(), name='download_template'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/<int:pk>/test/', CampaignSendTestView.as_view(), name='send_test'),
    path('campaign/<int:pk>/start/', CampaignStartSendingView.as_view(), name='start_sending'),
    path('campaign/<int:pk>/reset-status/', CampaignResetStatusView.as_view(), name='reset_status'),
    path('campaign/<int:pk>/validate-contacts/', CampaignValidateContactsView.as_view(), name='validate_contacts'),
    path('campaign/<int:pk>/prune-invalid/', CampaignPruneInvalidView.as_view(), name='prune_invalid'),
    path('api/campaign/<int:pk>/status/', CampaignStatusApiView.as_view(), name='campaign_status_api'),
    path('api/campaign/<int:pk>/dispatch-step/', CampaignDispatchStepApiView.as_view(), name='campaign_dispatch_step_api'),
    
    # Single / Custom Email Composer
    path('send-single/', SendSingleEmailView.as_view(), name='send_single'),
    
    # Centralized Email Logs
    path('emails-log/', EmailLogListView.as_view(), name='emails_log'),
    path('emails-log/<int:pk>/resend/', EmailLogResendView.as_view(), name='email_resend'),
    path('emails-log/<int:pk>/edit/', EmailLogEditView.as_view(), name='email_edit'),
    path('emails-log/<int:pk>/delete/', EmailLogDeleteView.as_view(), name='email_delete'),
    path('emails-log/resend-all-failed/', ResendAllFailedEmailsView.as_view(), name='resend_all_failed'),
    path('emails-log/sync-welcome/', SyncWelcomeLogsView.as_view(), name='sync_welcome_logs'),
]


