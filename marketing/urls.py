from django.urls import path
from .views import (
    DownloadTemplateView,
    CampaignDashboardView,
    CampaignDetailView,
    CampaignSendTestView,
    CampaignStartSendingView,
    CampaignStatusApiView,
)

app_name = 'marketing'

urlpatterns = [
    path('', CampaignDashboardView.as_view(), name='dashboard'),
    path('template/download/', DownloadTemplateView.as_view(), name='download_template'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/<int:pk>/test/', CampaignSendTestView.as_view(), name='send_test'),
    path('campaign/<int:pk>/start/', CampaignStartSendingView.as_view(), name='start_sending'),
    path('api/campaign/<int:pk>/status/', CampaignStatusApiView.as_view(), name='campaign_status_api'),
]
