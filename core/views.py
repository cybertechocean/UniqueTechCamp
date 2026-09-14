from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from .models import Testimonial, FAQ, ContactMessage
from services.models import Service
from portfolio.models import Project

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['projects'] = Project.objects.all()[:4]
        context['testimonials'] = Testimonial.objects.all()[:3]
        context['faqs'] = FAQ.objects.filter(is_active=True)[:5]
        return context

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message
            )
            messages.success(request, "Your message has been sent successfully. We will get back to you shortly.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'pages/contact.html', {
                'name': name, 'email': email, 'phone': phone,
                'subject': subject, 'message': message
            })
