import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .models import UserProfile
from .forms import (
    ClientRegistrationForm,
    ClientLoginForm,
    ClientProfileUpdateForm,
    generate_math_challenge
)
from .emails import send_verification_email
from .backends import EmailOrUsernameModelBackend
from core.emails import send_welcome_email

logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterView(View):
    """
    Ultra-Modern Client Registration View.
    Enforces human verification (math test), international phone numbers (+254...),
    and email verification flow.
    """
    template_name = 'accounts/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        
        question, _ = generate_math_challenge(request)
        form = ClientRegistrationForm(request=request)
        return render(request, self.template_name, {
            'form': form,
            'math_question': question,
        })

    def post(self, request):
        form = ClientRegistrationForm(request.POST, request=request)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            # User will be active, but flagged unverified until email confirmed
            user.is_active = True
            user.save()

            # Create client profile with international phone number
            phone_num = form.cleaned_data['phone_number']
            country_code = phone_num[:4] if phone_num.startswith('+254') else phone_num[:3]
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': phone_num,
                    'country_code': country_code,
                    'company_name': form.cleaned_data.get('company_name', ''),
                    'is_email_verified': False,
                }
            )
            if not created:
                profile.phone_number = phone_num
                profile.company_name = form.cleaned_data.get('company_name', '')
                profile.save()

            # Send Email Verification Link
            send_verification_email(user, request)

            # Store username in session for verification instructions page
            request.session['unverified_user_id'] = user.id
            request.session['unverified_email'] = user.email

            messages.success(
                request,
                f"Registration successful! We have sent a verification email to {user.email}. Please verify your account to unlock full access."
            )
            return redirect('accounts:verification_sent')
        
        # On validation error, generate a new math challenge
        question, _ = generate_math_challenge(request)
        return render(request, self.template_name, {
            'form': form,
            'math_question': question,
        })


class VerificationSentView(View):
    """Instruction page notifying user to check their email for verification link."""
    template_name = 'accounts/verification_sent.html'

    def get(self, request):
        email = request.session.get('unverified_email', '')
        return render(request, self.template_name, {
            'email': email,
        })


class VerifyEmailView(View):
    """
    Handles confirmation of email verification link.
    On success:
    1. Sets profile.is_email_verified = True
    2. Sends the branded Welcome Email to the client
    3. Logs client into their new account
    4. Redirects to client dashboard with celebration alert
    """
    template_name = 'accounts/verification_success.html'

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            profile = getattr(user, 'profile', None)
            if profile and profile.email_verification_token == token:
                # Mark as verified
                profile.is_email_verified = True
                profile.save(update_fields=['is_email_verified'])

                # Send High-Converting Branded Welcome Email
                if not profile.welcome_email_sent:
                    try:
                        send_welcome_email(
                            recipient_email=user.email,
                            user_name=user.get_full_name() or user.username,
                            user=user,
                            request=request
                        )
                        profile.welcome_email_sent = True
                        profile.save(update_fields=['welcome_email_sent'])
                    except Exception as e:
                        logger.error(f"Could not send welcome email: {e}")

                # Automatically log user in
                user.backend = 'accounts.backends.EmailOrUsernameModelBackend'
                login(request, user)

                messages.success(
                    request,
                    f"Welcome aboard, {user.first_name or user.username}! Your email has been verified successfully. Your welcome package has been sent to your inbox."
                )
                return render(request, self.template_name, {'user': user, 'verified': True})

        # Token invalid or expired
        return render(request, self.template_name, {'verified': False})


class ResendVerificationView(View):
    """Allows user to request a fresh email verification link."""
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        if not email and request.user.is_authenticated:
            email = request.user.email

        user = User.objects.filter(email__iexact=email).first()
        if user:
            profile = getattr(user, 'profile', None)
            if profile and not profile.is_email_verified:
                send_verification_email(user, request)
                messages.success(request, f"A fresh verification email has been sent to {email}.")
            elif profile and profile.is_email_verified:
                messages.info(request, "This account is already verified. You can log in directly.")
                return redirect('accounts:login')
        else:
            messages.info(request, "If that email is registered with us, a verification link has been sent.")

        return redirect('accounts:verification_sent')


class LoginView(View):
    """
    Ultra-Modern Client Login View.
    Supports login via Username OR Email address.
    """
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = ClientLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['login_identifier'].strip()
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)

            from django.contrib.auth import authenticate
            user = authenticate(request, username=identifier, password=password)

            if user is not None:
                login(request, user)
                
                # Session persistence
                if not remember_me:
                    request.session.set_expiry(0)  # Expires when browser closes
                else:
                    request.session.set_expiry(30 * 86400)  # 30 days

                # Verification reminder notice if still pending
                profile = getattr(user, 'profile', None)
                if profile and not profile.is_email_verified:
                    messages.warning(
                        request,
                        "Your email address is not yet verified. Please check your inbox or request a new verification link from your dashboard."
                    )
                else:
                    messages.success(request, f"Welcome back, {user.first_name or user.username}!")

                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('accounts:dashboard')
            else:
                messages.error(
                    request,
                    "Invalid username/email or password. Please check your credentials and try again."
                )

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Logs the client out and redirects to home with confirmation."""
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully. See you again soon!")
        return redirect('core:home')

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('core:home')


class ClientDashboardView(LoginRequiredMixin, View):
    """
    Ultra-Modern Client Management Studio Dashboard.
    Provides overview of:
    - Client details & email verification status
    - Saved / favorited AI Master Coding Prompts
    - Assistance request tickets
    - Safaricom Buy Goods Till: 5797853 payment support
    - Quick actions (browse prompts, book consultations)
    """
    template_name = 'accounts/dashboard.html'

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        saved_prompts = profile.saved_prompts.all()
        
        # Fetch any assistance requests for this client
        from ai_prompts.models import PromptAssistanceRequest
        assistance_requests = PromptAssistanceRequest.objects.filter(
            user=request.user
        ).order_by('-created_at')

        # Form for profile updates
        profile_form = ClientProfileUpdateForm(instance=request.user, profile=profile)

        context = {
            'profile': profile,
            'saved_prompts': saved_prompts,
            'assistance_requests': assistance_requests,
            'profile_form': profile_form,
            'mpesa_till': '5797853',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile_form = ClientProfileUpdateForm(request.POST, instance=request.user, profile=profile)

        if profile_form.is_valid():
            user = profile_form.save()
            profile.phone_number = profile_form.cleaned_data['phone_number']
            profile.company_name = profile_form.cleaned_data['company_name']
            profile.save()
            messages.success(request, "Your client profile was updated successfully.")
            return redirect('accounts:dashboard')

        saved_prompts = profile.saved_prompts.all()
        from ai_prompts.models import PromptAssistanceRequest
        assistance_requests = PromptAssistanceRequest.objects.filter(user=request.user).order_by('-created_at')

        return render(request, self.template_name, {
            'profile': profile,
            'saved_prompts': saved_prompts,
            'assistance_requests': assistance_requests,
            'profile_form': profile_form,
            'mpesa_till': '5797853',
        })


class RefreshMathChallengeApiView(View):
    """Dynamic API endpoint returning a freshly generated math problem."""
    def get(self, request):
        question, _ = generate_math_challenge(request)
        return JsonResponse({'question': question})
