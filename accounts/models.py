import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


# Validator ensuring phone numbers begin with '+' and country code (e.g., +254..., +1...)
phone_regex = RegexValidator(
    regex=r'^\+[1-9]\d{7,14}$',
    message="Phone number must start with a valid international country code (e.g., +254712345678 or +1234567890)."
)


class UserProfile(models.Model):
    """
    Ultra-Modern Client Profile model linked 1-to-1 with Django auth User.
    Enforces international phone numbers, email verification tracking, and saved resources.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(
        max_length=25,
        validators=[phone_regex],
        help_text="International format starting with country code e.g. +254715479955"
    )
    country_code = models.CharField(max_length=8, default="+254", blank=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    
    # Email Verification
    is_email_verified = models.BooleanField(
        default=False,
        help_text="Designates whether this client has verified their email address."
    )
    email_verification_token = models.CharField(
        max_length=64,
        blank=True,
        default=uuid.uuid4,
        help_text="Secure cryptographic verification token"
    )
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    welcome_email_sent = models.BooleanField(default=False)

    # Saved AI Coding Prompts
    saved_prompts = models.ManyToManyField(
        'ai_prompts.AIPrompt',
        blank=True,
        related_name='favorited_by_profiles',
        help_text="Prompts saved or bookmarked by this client"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
        ordering = ['-created_at']

    def __str__(self):
        full_name = self.user.get_full_name()
        display = full_name if full_name else self.user.username
        return f"{display} ({self.phone_number})"

    def generate_new_verification_token(self):
        """Generates a fresh token and updates the timestamp."""
        self.email_verification_token = uuid.uuid4().hex
        self.email_verification_sent_at = timezone.now()
        self.save(update_fields=['email_verification_token', 'email_verification_sent_at'])
        return self.email_verification_token

    @property
    def get_avatar_url(self):
        """Returns uploaded avatar if present, otherwise external URL or default Gravatar/UI avatar."""
        if self.avatar:
            try:
                return self.avatar.url
            except Exception:
                pass
        if self.avatar_url:
            return self.avatar_url
        # Fallback to high quality modern SVG avatar generated from client initials
        initials = (self.user.first_name[:1] + self.user.last_name[:1]) or self.user.username[:2]
        return f"https://ui-avatars.com/api/?name={initials}&background=059669&color=ffffff&bold=true&rounded=true"
