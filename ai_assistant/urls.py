from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    # Dedicated Full-Page Workspace
    path('', views.AiAssistantPageView.as_view(), name='index'),

    # REST / JSON API Endpoints
    path('api/init/', views.ChatInitApiView.as_view(), name='api_init'),
    path('api/message/', views.SendMessageApiView.as_view(), name='api_message'),
    path('api/capture-lead/', views.CaptureLeadApiView.as_view(), name='api_capture_lead'),
    path('api/availability/', views.CheckAvailabilityApiView.as_view(), name='api_availability'),
    path('api/book/', views.BookConsultationApiView.as_view(), name='api_book'),
    path('api/email-transcript/', views.EmailTranscriptApiView.as_view(), name='api_email_transcript'),
]
