from django import forms
from django.core.validators import RegexValidator
from .models import PromptAssistanceRequest, PromptPurchase

phone_regex = RegexValidator(
    regex=r'^\+[1-9]\d{7,14}$',
    message="Phone number must start with a valid international country code (e.g. +254...)."
)


class PromptAssistanceForm(forms.ModelForm):
    """
    Form for clients to request 1-on-1 assistance or custom setup
    with Safaricom Buy Goods Till: 5797853 tracking.
    """
    client_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Your Full Name'
        })
    )
    client_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'name@example.com'
        })
    )
    client_phone = forms.CharField(
        max_length=25,
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': '+254 715 479 955 (Must start with country code)'
        })
    )
    requirements = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'utc-form-input',
            'rows': 4,
            'placeholder': 'Tell us what you need help with (e.g. customized features, hosting setup, WhatsApp bot connection, Google Sheets formula integration)...'
        })
    )
    mpesa_reference = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input font-mono font-bold uppercase tracking-wider',
            'placeholder': 'e.g. SHG897XYZ (M-Pesa reference code)'
        }),
        help_text="If you have completed payment to Till: 5797853, paste your M-Pesa transaction code here."
    )

    class Meta:
        model = PromptAssistanceRequest
        fields = ['client_name', 'client_email', 'client_phone', 'requirements', 'mpesa_reference']


class PromptPaymentSubmissionForm(forms.ModelForm):
    """
    Form for clients to submit payment proof (M-Pesa code, SMS message,
    screenshot upload, or alternative payment requests) for paid AI Prompts.
    """
    client_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Your Full Name'
        })
    )
    client_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'name@example.com (Access link & receipt will be sent here)'
        })
    )
    client_phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': '+254 715 479 955 (WhatsApp / Phone)'
        })
    )
    payment_method = forms.ChoiceField(
        choices=PromptPurchase.PAYMENT_METHODS,
        required=True,
        widget=forms.Select(attrs={
            'class': 'utc-form-input',
            'id': 'id_payment_method_select'
        })
    )
    transaction_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input font-mono font-bold uppercase tracking-wider',
            'placeholder': 'e.g. UII9O6P15V (M-Pesa code)'
        })
    )
    payment_message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'utc-form-input font-mono text-xs',
            'rows': 3,
            'placeholder': 'Optional: Paste full M-Pesa SMS confirmation message or transaction notes here...'
        })
    )
    payment_screenshot = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'utc-form-input text-xs file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-emerald-500 file:text-slate-950 hover:file:bg-emerald-400 cursor-pointer',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = PromptPurchase
        fields = ['client_name', 'client_email', 'client_phone', 'payment_method', 'transaction_code', 'payment_message', 'payment_screenshot']
