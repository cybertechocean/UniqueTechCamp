from django.urls import path
from .views import AppointmentBookView, AppointmentSuccessView, DownloadIcsView

app_name = 'appointments'

urlpatterns = [
    path('', AppointmentBookView.as_view(), name='book'),
    path('success/<str:reference>/', AppointmentSuccessView.as_view(), name='success'),
    path('calendar/<str:reference>/ics/', DownloadIcsView.as_view(), name='download_ics'),
]
