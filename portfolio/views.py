from django.views.generic import ListView, DetailView
from .models import Project

class PortfolioListView(ListView):
    model = Project
    template_name = 'portfolio/list.html'
    context_object_name = 'projects'

class PortfolioDetailView(DetailView):
    model = Project
    template_name = 'portfolio/detail.html'
    context_object_name = 'project'
