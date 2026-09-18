import random
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, phone_regex


def generate_math_challenge(request):
    """
    Generates a dynamic addition or subtraction challenge stored in session.
    Returns (question_string, expected_answer_int).
    """
    operations = ['+', '-']
    op = random.choice(operations)
    
    if op == '+':
        n1 = random.randint(3, 18)
        n2 = random.randint(2, 15)
        ans = n1 + n2
        question = f"{n1} + {n2}"
    else:
        n1 = random.randint(10, 25)
        n2 = random.randint(1, n1 - 1)
        ans = n1 - n2
        question = f"{n1} - {n2}"

    if request:
        request.session['utc_math_answer'] = str(ans)
        request.session['utc_math_question'] = question
        request.session.modified = True

    return question, ans


class ClientRegistrationForm(forms.ModelForm):
    """
    Ultra-Modern Registration form with:
    1. First & Last name
    2. Unique username & email
    3. Mandatory international phone number starting with country code (+254...)
    4. Password & confirmation
    5. Server-verified math challenge (human verification)
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'First Name (e.g. Alex)'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Last Name (e.g. Mwangi)'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'name@example.com'
        })
    )
    phone_number = forms.CharField(
        max_length=25,
        required=True,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': '+254 715 479 955 (Must start with country code)'
        }),
        help_text="Include your international country code starting with + (e.g. +254 for Kenya, +1 for USA/Canada, +44 for UK)."
    )
    company_name = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Company / Brand Name (Optional)'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Create a secure password (min 8 chars)'
        }),
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Re-enter your password'
        })
    )
    math_answer = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input text-center font-bold tracking-widest',
            'placeholder': 'Your Answer'
        }),
        help_text="Human verification: Solve this simple math problem."
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'utc-form-input',
                'placeholder': 'Unique Username (e.g. alexmwangi)'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please pick another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists. Please log in.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').replace(' ', '').strip()
        if not phone.startswith('+'):
            raise ValidationError("Phone number must begin with a '+' and your country code (e.g. +254 for Kenya).")
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise ValidationError("This phone number is already registered. Please sign in or use another number.")
        return phone

    def clean_math_answer(self):
        user_ans = self.cleaned_data.get('math_answer', '').strip()
        expected = None
        if self.request:
            expected = self.request.session.get('utc_math_answer')
        
        if not expected or str(user_ans) != str(expected):
            raise ValidationError("Incorrect math answer. Please verify you are human and try again.")
        return user_ans

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')

        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Passwords do not match. Please verify and re-type.")

        return cleaned_data


class ClientLoginForm(forms.Form):
    """
    Login form allowing clients to log in via Username OR Email Address.
    """
    login_identifier = forms.CharField(
        label="Username or Email Address",
        widget=forms.TextInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Enter your username or email',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'utc-form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded border-slate-700 text-emerald-500 focus:ring-emerald-500'
        })
    )


class ClientProfileUpdateForm(forms.ModelForm):
    """Form for client to update their personal details."""
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(max_length=25, required=True, validators=[phone_regex])
    company_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        if self.profile:
            self.fields['phone_number'].initial = self.profile.phone_number
            self.fields['company_name'].initial = self.profile.company_name
