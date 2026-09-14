import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Testimonial, FAQ, ContactMessage
from services.models import Service, ServiceCategory
from portfolio.models import Project
from blog.models import Post

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)[:8]
        context['projects'] = Project.objects.all()[:4]
        context['testimonials'] = Testimonial.objects.all()[:3]
        context['faqs'] = FAQ.objects.filter(is_active=True)[:6]
        context['latest_posts'] = Post.objects.filter(is_published=True)[:3]
        return context

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class CookiePolicyView(TemplateView):
    template_name = 'pages/cookie_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'pages/terms_of_service.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy_policy.html'

class PaymentPolicyView(TemplateView):
    template_name = 'pages/payment_policy.html'

class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact.html')

    def post(self, request):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and subject and message:
            # 1. Save to Database
            contact_msg = ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message
            )

            # 2. Dispatch SMTP Notification Emails
            try:
                # Admin Notification
                admin_recipients = [
                    getattr(settings, 'ADMIN_EMAIL_PRIMARY', 'info@uniquetechcamp.org'),
                    getattr(settings, 'ADMIN_EMAIL_GMAIL', 'UniqueTechCamp@gmail.com')
                ]
                admin_subject = f"[New Lead] {subject} - {name}"
                admin_body = (
                    f"New Inquiry Received from UniqueTechCamp Website:\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone or 'Not provided'}\n"
                    f"Subject: {subject}\n\n"
                    f"Message:\n{message}\n\n"
                    f"Timestamp: {contact_msg.created_at}\n"
                )
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'UniqueTechCamp <info@uniquetechcamp.org>')
                
                # Send to admins
                send_mail(
                    subject=admin_subject,
                    message=admin_body,
                    from_email=from_email,
                    recipient_list=admin_recipients,
                    fail_silently=True
                )

                # Client Confirmation Auto-Responder
                client_subject = f"Thank you for contacting UniqueTechCamp - {subject}"
                client_body = (
                    f"Hello {name},\n\n"
                    f"Thank you for reaching out to UniqueTechCamp! We have received your inquiry regarding '{subject}'.\n\n"
                    f"Our technical solutions team is reviewing your project details. A solutions architect will get back to you within a few business hours via email or WhatsApp ({phone or 'your provided contact'}).\n\n"
                    f"If your project requires urgent discussion, you may also connect directly on WhatsApp at +254 715 479 955.\n\n"
                    f"Best regards,\n"
                    f"The UniqueTechCamp Team\n"
                    f"Web Development • AI Systems • Digital Growth\n"
                    f"https://uniquetechcamp.org\n"
                )
                send_mail(
                    subject=client_subject,
                    message=client_body,
                    from_email=from_email,
                    recipient_list=[email],
                    fail_silently=True
                )
            except Exception as e:
                logger.warning(f"SMTP notification dispatch skipped or encountered non-fatal error: {e}")

            messages.success(request, "Your message has been sent successfully. We will get back to you shortly.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'pages/contact.html', {
                'name': name, 'email': email, 'phone': phone,
                'subject': subject, 'message': message
            })

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        services = []
        blog_posts = []
        projects = []
        policy_matches = []

        if query:
            # 1. Services
            services = Service.objects.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(overview__icontains=query) |
                Q(benefits__icontains=query) |
                Q(category__name__icontains=query),
                is_active=True
            ).select_related('category')[:12]

            # 2. Blog Posts
            blog_posts = Post.objects.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__icontains=query),
                is_published=True
            ).select_related('category')[:6]

            # 3. Projects
            projects = Project.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(technologies__icontains=query) |
                Q(client_name__icontains=query)
            )[:6]

            # 4. Policy check
            policies = [
                {'title': 'Payment Policy', 'url': '/payment-policy/', 'keywords': ['payment', 'mpesa', 'm-pesa', 'bank', 'card', 'invoice', 'milestone', 'deposit', 'refund', 'fee', 'charge']},
                {'title': 'Privacy Policy', 'url': '/privacy/', 'keywords': ['privacy', 'data', 'gdpr', 'security', 'dpa', 'cookies', 'encryption', 'personal', 'information']},
                {'title': 'Terms of Service', 'url': '/terms/', 'keywords': ['terms', 'service', 'contract', 'agreement', 'sla', 'warranty', 'intellectual property', 'code ownership', 'dispute']},
                {'title': 'Cookie Policy', 'url': '/cookies/', 'keywords': ['cookie', 'tracking', 'pixel', 'session', 'storage', 'analytics']},
            ]
            q_lower = query.lower()
            for p in policies:
                if any(kw in q_lower for kw in p['keywords']) or p['title'].lower() in q_lower:
                    policy_matches.append({
                        'title': p['title'],
                        'url': p['url'],
                        'snippet': f"View official UniqueTechCamp {p['title']} and compliance standards."
                    })

        total_results = len(services) + len(blog_posts) + len(projects) + len(policy_matches)

        return render(request, 'pages/search.html', {
            'query': query,
            'services': services,
            'blog_posts': blog_posts,
            'projects': projects,
            'policy_matches': policy_matches,
            'total_results': total_results,
        })

class SearchApiView(View):
    """
    Ultra-fast JSON endpoint returning instant suggestions as the user types
    """
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if len(query) < 2:
            return JsonResponse({'results': [], 'count': 0})

        suggestions = []

        # 1. Matching Services
        services = Service.objects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(short_description__icontains=query),
            is_active=True
        ).select_related('category')[:6]

        for s in services:
            suggestions.append({
                'title': s.title,
                'type': 'Service',
                'badge': s.category.name if s.category else 'Growth System',
                'url': f"/services/{s.slug}/",
                'snippet': s.short_description[:100] + '...',
                'icon': 'layers',
            })

        # 2. Matching Blog Posts
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query),
            is_published=True
        )[:3]

        for p in posts:
            suggestions.append({
                'title': p.title,
                'type': 'Article',
                'badge': p.category.name if p.category else 'Blog',
                'url': p.get_absolute_url(),
                'snippet': p.excerpt[:90] + '...' if p.excerpt else 'Read our latest tech insights.',
                'icon': 'book-open',
            })

        # 3. Matching Projects
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(client_name__icontains=query)
        )[:2]

        for proj in projects:
            suggestions.append({
                'title': proj.title,
                'type': 'Project',
                'badge': 'Case Study',
                'url': f"/portfolio/{proj.slug}/",
                'snippet': f"Client: {proj.client_name}",
                'icon': 'briefcase',
            })

        # 4. Matching Policies
        q_lower = query.lower()
        if any(w in q_lower for w in ['pay', 'mpesa', 'price', 'cost', 'invoice', 'milestone', 'deposit', 'refund']):
            suggestions.append({
                'title': 'Commercial Payment Policy & Milestones',
                'type': 'Policy',
                'badge': 'Financial Terms',
                'url': '/payment-policy/',
                'snippet': 'M-Pesa, Bank Wire, Milestone schedules, and settlement terms.',
                'icon': 'credit-card',
            })
        if any(w in q_lower for w in ['priv', 'data', 'gdpr', 'security']):
            suggestions.append({
                'title': 'Privacy Policy & Data Protection',
                'type': 'Policy',
                'badge': 'Compliance',
                'url': '/privacy/',
                'snippet': 'Kenya DPA 2019 & GDPR data handling commitments.',
                'icon': 'shield-check',
            })
        if any(w in q_lower for w in ['term', 'agree', 'sla', 'warrant', 'contract', 'code own']):
            suggestions.append({
                'title': 'Terms of Service & Code Ownership',
                'type': 'Policy',
                'badge': 'Legal Agreement',
                'url': '/terms/',
                'snippet': 'SOW specifications, client code transfer, and 30-day warranty.',
                'icon': 'file-text',
            })
        if any(w in q_lower for w in ['cookie', 'track']):
            suggestions.append({
                'title': 'Cookie Policy & Web Storage',
                'type': 'Policy',
                'badge': 'Transparency',
                'url': '/cookies/',
                'snippet': 'Cookie types, preferences, and session controls.',
                'icon': 'cookie',
            })

        return JsonResponse({
            'results': suggestions,
            'count': len(suggestions),
            'query': query,
        })
