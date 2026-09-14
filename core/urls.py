from django.urls import path
from .views import (
    HomeView, AboutView, ContactView,
    CookiePolicyView, TermsOfServiceView, PrivacyPolicyView, PaymentPolicyView,
    SearchView, SearchApiView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('cookies/', CookiePolicyView.as_view(), name='cookie_policy'),
    path('terms/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('payment-policy/', PaymentPolicyView.as_view(), name='payment_policy'),
    path('search/', SearchView.as_view(), name='search'),
    path('api/search/', SearchApiView.as_view(), name='search_api'),
]
