from django import forms
from django.core.validators import RegexValidator
from .models import PromptAssistanceRequest

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
    requirements = forms.TextField = forms.CharField(
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
