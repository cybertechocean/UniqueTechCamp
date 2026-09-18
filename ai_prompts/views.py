import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import AIPrompt, PromptCategory, PromptAssistanceRequest, PromptPurchase
from .forms import PromptAssistanceForm, PromptPaymentSubmissionForm

logger = logging.getLogger(__name__)


def check_user_prompt_access(request, prompt):
    """
    Determines whether the client has verified access to view, copy,
    and download this AI Master Coding Prompt.
    """
    if prompt.is_free:
        return True
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return True
    if request.user.is_authenticated:
        # Check verified purchase by user object or client email
        return PromptPurchase.objects.filter(
            prompt=prompt,
            is_verified=True
        ).filter(Q(user=request.user) | Q(client_email__iexact=request.user.email)).exists()
    else:
        # Check session email
        session_email = request.session.get(f'prompt_verified_email_{prompt.id}')
        if session_email:
            return PromptPurchase.objects.filter(
                prompt=prompt,
                client_email__iexact=session_email,
                is_verified=True
            ).exists()
    return False


class PromptListView(View):
    """
    Catalog / Marketplace view of all AI Master Coding Prompts.
    Supports filtering by category, free vs paid, search queries, and currency mode (KES vs USD).
    """
    template_name = 'ai_prompts/prompt_list.html'

    def get(self, request):
        prompts = AIPrompt.objects.filter(is_published=True).select_related('category')
        categories = PromptCategory.objects.all()

        # Category Filter
        category_slug = request.GET.get('category')
        selected_category = None
        if category_slug:
            selected_category = get_object_or_404(PromptCategory, slug=category_slug)
            prompts = prompts.filter(category=selected_category)

        # Price Filter
        price_filter = request.GET.get('pricing', 'all')
        if price_filter == 'free':
            prompts = prompts.filter(is_free=True)
        elif price_filter == 'paid':
            prompts = prompts.filter(is_free=False)

        # Search Query
        query = request.GET.get('q', '').strip()
        if query:
            prompts = prompts.filter(
                Q(title__icontains=query) |
                Q(tagline__icontains=query) |
                Q(overview__icontains=query) |
                Q(tech_stack__icontains=query) |
                Q(target_ai_tools__icontains=query)
            )

        # Sorting
        sort = request.GET.get('sort', 'featured')
        if sort == 'newest':
            prompts = prompts.order_by('-created_at')
        elif sort == 'popular':
            prompts = prompts.order_by('-copy_count', '-view_count')
        elif sort == 'price_low':
            prompts = prompts.order_by('price_kes')
        elif sort == 'price_high':
            prompts = prompts.order_by('-price_kes')
        else:
            prompts = prompts.order_by('-is_featured', '-copy_count', '-created_at')

        # Currency Preference (default KES)
        active_currency = request.GET.get('currency', request.session.get('utc_currency', 'KES'))
        if active_currency in ['KES', 'USD']:
            request.session['utc_currency'] = active_currency

        context = {
            'prompts': prompts,
            'categories': categories,
            'selected_category': selected_category,
            'active_pricing': price_filter,
            'search_query': query,
            'active_currency': active_currency,
            'mpesa_till': '5797853',
            'total_prompts_count': prompts.count(),
        }
        return render(request, self.template_name, context)


class PromptDetailView(View):
    """
    Detailed Product Page for an AI Master Coding Prompt.
    Features YouTube embed/preview, dual currency pricing, copy prompt trigger,
    prompt download, and Safaricom Till 5797853 payment & assistance forms.
    """
    template_name = 'ai_prompts/prompt_detail.html'

    def get(self, request, slug):
        prompt = get_object_or_404(AIPrompt, slug=slug, is_published=True)

        # Increment view count
        AIPrompt.objects.filter(pk=prompt.pk).update(view_count=F('view_count') + 1)
        prompt.refresh_from_db(fields=['view_count'])

        # Related prompts in same category
        related_prompts = AIPrompt.objects.filter(
            category=prompt.category,
            is_published=True
        ).exclude(pk=prompt.pk)[:3]

        # Check if saved by current user (safe profile retrieval without RelatedObjectDoesNotExist)
        is_saved = False
        user_phone = ''
        if request.user.is_authenticated:
            from accounts.models import UserProfile
            user_prof = UserProfile.objects.filter(user=request.user).first()
            if user_prof:
                is_saved = user_prof.saved_prompts.filter(pk=prompt.pk).exists()
                user_phone = user_prof.phone_number or ''

        # Pre-fill forms if user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'client_name': request.user.get_full_name() or request.user.username,
                'client_email': request.user.email,
                'client_phone': user_phone,
            }
        assistance_form = PromptAssistanceForm(initial=initial_data)
        payment_form = PromptPaymentSubmissionForm(initial=initial_data)

        # Verify access rights
        has_access = check_user_prompt_access(request, prompt)
        pending_purchase = None
        if not has_access:
            if request.user.is_authenticated:
                pending_purchase = PromptPurchase.objects.filter(
                    prompt=prompt,
                    is_verified=False,
                    status='pending'
                ).filter(Q(user=request.user) | Q(client_email__iexact=request.user.email)).first()
            else:
                submitted_email = request.session.get(f'prompt_submitted_email_{prompt.id}')
                if submitted_email:
                    pending_purchase = PromptPurchase.objects.filter(
                        prompt=prompt,
                        client_email__iexact=submitted_email,
                        is_verified=False,
                        status='pending'
                    ).first()

        # Currency preference
        active_currency = request.GET.get('currency', request.session.get('utc_currency', 'KES'))

        context = {
            'prompt': prompt,
            'related_prompts': related_prompts,
            'is_saved': is_saved,
            'has_access': has_access,
            'pending_purchase': pending_purchase,
            'payment_form': payment_form,
            'assistance_form': assistance_form,
            'mpesa_till': '5797853',
            'active_currency': active_currency,
        }
        return render(request, self.template_name, context)


class CopyPromptApiView(View):
    """AJAX endpoint to record copy event and increment prompt copy count."""
    def post(self, request, slug):
        prompt = get_object_or_404(AIPrompt, slug=slug, is_published=True)

        if not check_user_prompt_access(request, prompt):
            return JsonResponse({
                'success': False,
                'error': 'Payment verification required to copy this premium master prompt. Please submit your payment reference or contact our desk.'
            }, status=403)

        AIPrompt.objects.filter(pk=prompt.pk).update(copy_count=F('copy_count') + 1)
        prompt.refresh_from_db(fields=['copy_count'])

        return JsonResponse({
            'success': True,
            'copy_count': prompt.copy_count,
            'message': 'AI Master Coding Prompt copied to clipboard!'
        })


class DownloadPromptView(View):
    """Serves prompt as a clean downloadable text or markdown file."""
    def get(self, request, slug):
        prompt = get_object_or_404(AIPrompt, slug=slug, is_published=True)

        if not check_user_prompt_access(request, prompt):
            messages.warning(
                request,
                "Payment verification is required to download this premium AI Master Coding Prompt. "
                "Please submit your M-Pesa transaction reference or reach out to our solutions desk."
            )
            return redirect(prompt.get_absolute_url())

        AIPrompt.objects.filter(pk=prompt.pk).update(download_count=F('download_count') + 1)

        file_content = f"""# {prompt.title}
# UniqueTechCamp — Master AI Coding Prompt
# Category: {prompt.category.name}
# Tech Stack: {prompt.tech_stack}
# Target AI Tools: {prompt.target_ai_tools}
# Safaricom Till for Custom Setup: 5797853 (UniqueTechCamp)
# Web: https://uniquetechcamp.org/ai-project-prompts/{prompt.slug}/

================================================================================
STEP-BY-STEP SYSTEM INSTRUCTIONS
================================================================================
{prompt.system_instructions or "Execute this master prompt in Claude Code, Cursor, Windsurf, or ChatGPT."}

================================================================================
MASTER AI CODING PROMPT
================================================================================
{prompt.master_prompt}

================================================================================
NEED 1-ON-1 SETUP OR CUSTOM ADAPTATION?
================================================================================
UniqueTechCamp engineers and assists you in customizing and deploying this solution:
- Safaricom Buy Goods Till: 5797853
- WhatsApp Consultation: +254 715 479 955
- Email: info@uniquetechcamp.org
"""
        response = HttpResponse(file_content, content_type='text/markdown; charset=utf-8')
        filename = f"{prompt.slug}-master-prompt.md"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class PromptPaymentSubmitView(View):
    """
    Processes client submission of M-Pesa transaction code, SMS message,
    or screenshot for verification in Django Admin.
    """
    def post(self, request, slug):
        prompt = get_object_or_404(AIPrompt, slug=slug, is_published=True)
        form = PromptPaymentSubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.prompt = prompt
            if request.user.is_authenticated:
                purchase.user = request.user
            purchase.amount_paid = prompt.price_kes
            purchase.currency = 'KES'
            purchase.status = 'pending'
            purchase.is_verified = False
            purchase.save()

            # Store in session so anonymous users can track status
            request.session[f'prompt_submitted_email_{prompt.id}'] = purchase.client_email

            # Dispatch real-time admin alert to management in background thread (or inline during tests)
            from ai_assistant.views import run_async_or_inline
            from .emails import send_prompt_purchase_admin_alert
            run_async_or_inline(send_prompt_purchase_admin_alert, purchase)

            messages.success(
                request,
                f"Thank you, {purchase.client_name}! Your payment submission (Ref: {purchase.transaction_code or purchase.get_payment_method_display()}) "
                "has been received by our Solutions Architecture management team. Once verified in our system (typically 15–30 minutes), "
                f"your prompt will unlock automatically and you will receive confirmation at {purchase.client_email}."
            )
            return redirect(prompt.get_absolute_url())
        else:
            messages.error(request, "Please check the payment submission form and ensure all required fields are filled.")
            return redirect(prompt.get_absolute_url())


class ToggleSavePromptView(LoginRequiredMixin, View):
    """Saves or unsaves a prompt to the client's profile."""
    def post(self, request, slug):
        prompt = get_object_or_404(AIPrompt, slug=slug, is_published=True)
        profile = getattr(request.user, 'profile', None)
        if not profile:
            from accounts.models import UserProfile
            profile = UserProfile.objects.create(user=request.user)

        if profile.saved_prompts.filter(pk=prompt.pk).exists():
            profile.saved_prompts.remove(prompt)
            saved = False
            message = "Prompt removed from saved list."
        else:
            profile.saved_prompts.add(prompt)
            saved = True
            message = "Prompt saved to your Client Dashboard!"

        return JsonResponse({
            'success': True,
            'saved': saved,
            'message': message,
        })


class PromptAssistanceSubmitView(View):
    """Handles 1-on-1 assistance request submission for an AI Prompt."""
    def post(self, request, slug):
        prompt = get_object_or_404(AIPrompt, slug=slug, is_published=True)
        form = PromptAssistanceForm(request.POST)

        if form.is_valid():
            req_obj = form.save(commit=False)
            req_obj.prompt = prompt
            if request.user.is_authenticated:
                req_obj.user = request.user
            
            # Record fee
            req_obj.amount_paid = prompt.assistance_price_kes
            req_obj.currency = 'KES'
            req_obj.save()

            messages.success(
                request,
                f"Thank you, {req_obj.client_name}! Your assistance request for '{prompt.title[:35]}...' has been received. Our solutions desk has been notified and will reach out via phone/WhatsApp ({req_obj.client_phone}) within 2 hours."
            )
            return redirect(prompt.get_absolute_url())

        messages.error(request, "Please check the form for errors and resubmit.")
        return redirect(prompt.get_absolute_url())
