from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.emails import send_welcome_email, send_password_reset_email

User = get_user_model()

class Command(BaseCommand):
    help = "Test and dispatch branded Welcome and Password Reset emails."

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            default='all',
            choices=['welcome', 'password_reset', 'all'],
            help='Type of email to dispatch: welcome, password_reset, or all'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='info@uniquetechcamp.org',
            help='Recipient email address for test dispatch'
        )
        parser.add_argument(
            '--console',
            action='store_true',
            help='Output email to console instead of sending via SMTP'
        )

    def handle(self, *args, **options):
        from django.conf import settings
        if options.get('console'):
            settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
            self.stdout.write(self.style.WARNING("Console email backend enabled (emails will print below)."))

        email_type = options['type']
        target_email = options['email']

        self.stdout.write(self.style.NOTICE(f"Initiating test email dispatch to: {target_email}"))

        # Find or create mock user object
        user = User.objects.filter(email=target_email).first()
        if not user:
            user = User.objects.first()
            if not user:
                user = User(username="testuser", email=target_email, first_name="Alex", last_name="Mwangi")

        if email_type in ['welcome', 'all']:
            self.stdout.write("Sending Welcome Email (with logo at top & social links at bottom)...")
            success = send_welcome_email(
                recipient_email=target_email,
                user_name=user.get_full_name() or "Valued Partner",
                user=user,
            )
            if success:
                self.stdout.write(self.style.SUCCESS("[OK] Welcome Email successfully dispatched!"))
            else:
                self.stdout.write(self.style.ERROR("[FAILED] Failed to dispatch Welcome Email (check SMTP credentials in .env)."))

        if email_type in ['password_reset', 'all']:
            self.stdout.write("Sending Password Reset Email (with logo at top & social links at bottom)...")
            user.email = target_email
            success = send_password_reset_email(user=user)
            if success:
                self.stdout.write(self.style.SUCCESS("[OK] Password Reset Email successfully dispatched!"))
            else:
                self.stdout.write(self.style.ERROR("[FAILED] Failed to dispatch Password Reset Email (check SMTP credentials in .env)."))

        self.stdout.write(self.style.SUCCESS("\nEmail dispatch test completed."))
