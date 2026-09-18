import re
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class PromptCategory(models.Model):
    """Category grouping for AI Master Coding Prompts."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        default='code',
        help_text="Lucide or Material icon name e.g. code, table, bot, shopping-bag, layout"
    )
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Prompt Category"
        verbose_name_plural = "Prompt Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AIPrompt(models.Model):
    """
    Detailed AI Master Coding Prompt product/service.
    Provides complete master coding prompts for Claude Code, Cursor, Windsurf, ChatGPT, etc.
    Dual currency pricing in KES and USD, 1-on-1 assistance pricing, and video walkthrough support.
    """
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Master', 'Master / Enterprise'),
    ]

    category = models.ForeignKey(
        PromptCategory,
        on_delete=models.CASCADE,
        related_name='prompts'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    tagline = models.CharField(
        max_length=300,
        help_text="Catchy 1-sentence value proposition"
    )
    overview = models.TextField(
        help_text="Detailed project description, architecture overview, and what gets built"
    )

    # Core AI Master Coding Prompt
    master_prompt = models.TextField(
        help_text="The DETAILED AI MASTER CODING PROMPT ready to paste into Claude Code, Cursor, Windsurf, etc."
    )
    system_instructions = models.TextField(
        blank=True,
        help_text="Step-by-step instructions on executing the prompt in AI tools"
    )
    features_list = models.TextField(
        blank=True,
        help_text="Bulleted list of key system features (1 feature per line)"
    )
    prerequisites = models.TextField(
        blank=True,
        help_text="Accounts, APIs, or tools needed (e.g. Google Cloud, Node.js, Claude API key)"
    )
    tech_stack = models.CharField(
        max_length=255,
        default="Google Apps Script, Claude Code, HTML5, Tailwind CSS",
        help_text="Comma-separated tech stack badges"
    )
    target_ai_tools = models.CharField(
        max_length=255,
        default="Claude Code, Cursor, Windsurf, ChatGPT-4o, Gemini",
        help_text="Tools optimized for this prompt"
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='Intermediate'
    )

    # Pricing & Nairobi Currency (KES / USD)
    is_free = models.BooleanField(
        default=False,
        help_text="Check if prompt is 100% free to copy and download"
    )
    price_kes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Price in Kenya Shillings (KES)"
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Price in US Dollars (USD)"
    )

    # 1-on-1 Assistance Pricing (Help them build/deploy at a cost)
    assistance_price_kes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=2500.00,
        help_text="1-on-1 personalized setup & customization fee (KES)"
    )
    assistance_price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=25.00,
        help_text="1-on-1 personalized setup & customization fee (USD)"
    )

    # Media & Demos (Inspired by Rameez Scripts)
    youtube_url = models.URLField(
        blank=True,
        null=True,
        help_text="Full YouTube URL or embed link (e.g. https://www.youtube.com/watch?v=...)"
    )
    live_demo_url = models.URLField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='prompts/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    # Popularity Metrics
    copy_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    # Status & Flags
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "AI Master Coding Prompt"
        verbose_name_plural = "AI Master Coding Prompts"
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        pricing = "FREE" if self.is_free else f"KES {self.price_kes:,.0f} / ${self.price_usd:,.0f}"
        return f"{self.title} [{pricing}]"

    def get_absolute_url(self):
        return reverse('ai_prompts:detail', kwargs={'slug': self.slug})

    @property
    def youtube_embed_id(self):
        """Extracts YouTube video ID for responsive iframe player."""
        if not self.youtube_url:
            return None
        match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', self.youtube_url)
        return match.group(1) if match else None

    @property
    def get_thumbnail_url(self):
        """Returns uploaded image, external URL, or YouTube maxresdefault thumbnail."""
        if self.featured_image:
            try:
                return self.featured_image.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        yt_id = self.youtube_embed_id
        if yt_id:
            return f"https://img.youtube.com/vi/{yt_id}/maxresdefault.jpg"
        return "/static/images/logo-rounded.png"

    @property
    def tech_stack_list(self):
        """Splits comma-separated tech stack string into clean list of tags."""
        if not self.tech_stack:
            return []
        return [item.strip() for item in self.tech_stack.split(',') if item.strip()]

    @property
    def ai_tools_list(self):
        """Splits comma-separated AI tools into clean list."""
        if not self.target_ai_tools:
            return []
        return [tool.strip() for tool in self.target_ai_tools.split(',') if tool.strip()]

    @property
    def features_as_list(self):
        """Returns features split by line breaks."""
        if not self.features_list:
            return []
        return [line.strip().lstrip('•-* ') for line in self.features_list.split('\n') if line.strip()]


class PromptAssistanceRequest(models.Model):
    """
    Client request for 1-on-1 assistance / custom adaptation / deployment
    with Safaricom Buy Goods Till: 5797853 reference.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('in_progress', 'In Progress / Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    prompt = models.ForeignKey(
        AIPrompt,
        on_delete=models.CASCADE,
        related_name='assistance_requests'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prompt_assistance_requests'
    )
    client_name = models.CharField(max_length=150)
    client_email = models.EmailField()
    client_phone = models.CharField(
        max_length=30,
        help_text="Phone number starting with country code e.g. +254..."
    )
    requirements = models.TextField(
        help_text="Describe what customizations, features, or setup help you need"
    )
    
    # Safaricom Buy Goods Till: 5797853 tracking
    mpesa_reference = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="M-Pesa transaction reference from Till 5797853"
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    currency = models.CharField(max_length=6, default='KES')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    admin_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prompt Assistance Request"
        verbose_name_plural = "Prompt Assistance Requests"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} - {self.prompt.title[:30]} [{self.status}]"
