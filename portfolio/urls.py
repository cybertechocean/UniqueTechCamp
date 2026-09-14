from django.urls import path
from .views import PortfolioListView, PortfolioDetailView

app_name = 'portfolio'

urlpatterns = [
    path('', PortfolioListView.as_view(), name='list'),
    path('<slug:slug>/', PortfolioDetailView.as_view(), name='detail'),
]
