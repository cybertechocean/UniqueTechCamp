from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    ClientDashboardView,
    VerificationSentView,
    VerifyEmailView,
    ResendVerificationView,
    RefreshMathChallengeApiView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', ClientDashboardView.as_view(), name='dashboard'),
    path('verification-sent/', VerificationSentView.as_view(), name='verification_sent'),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('resend-verification/', ResendVerificationView.as_view(), name='resend_verification'),
    path('api/refresh-math/', RefreshMathChallengeApiView.as_view(), name='refresh_math'),
]
