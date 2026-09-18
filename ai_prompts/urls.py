from django.urls import path
from .views import (
    PromptListView,
    PromptDetailView,
    CopyPromptApiView,
    DownloadPromptView,
    ToggleSavePromptView,
    PromptAssistanceSubmitView,
)

app_name = 'ai_prompts'

urlpatterns = [
    path('', PromptListView.as_view(), name='list'),
    path('<slug:slug>/', PromptDetailView.as_view(), name='detail'),
    path('api/copy/<slug:slug>/', CopyPromptApiView.as_view(), name='copy_api'),
    path('download/<slug:slug>/', DownloadPromptView.as_view(), name='download'),
    path('api/bookmark/<slug:slug>/', ToggleSavePromptView.as_view(), name='bookmark_api'),
    path('assist/<slug:slug>/', PromptAssistanceSubmitView.as_view(), name='assist_submit'),
]
