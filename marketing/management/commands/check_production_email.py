import os
import sys
import socket
import smtplib
import ssl
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from marketing.models import EmailLog
from marketing.email_service import get_email_connection, send_robust_email


class Command(BaseCommand):
    help = "Diagnoses SMTP connection, tests Google App Password authentication, and inspects recent production EmailLogs."

    def add_arguments(self, parser):
        parser.add_argument(
            '--send-to',
            type=str,
            help="Optionally send a live test email to this address using Email 2 (Google App Password)",
            default=None,
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=" * 70))
        self.stdout.write(self.style.NOTICE("  UNIQUETECHCAMP PRODUCTION EMAIL DIAGNOSTICS & LOG INSPECTOR"))
        self.stdout.write(self.style.NOTICE("=" * 70))

        # ----------------------------------------------------------------------
        # 1. ENVIRONMENT & CONFIGURATION
        # ----------------------------------------------------------------------
        self.stdout.write(self.style.HTTP_INFO("\n[1] Environment & Configuration Overview:"))
        self.stdout.write(f"  * Python Executable: {sys.executable}")
        self.stdout.write(f"  * Python Version   : {sys.version.split()[0]}")
        self.stdout.write(f"  * Operating System : {os.name} ({sys.platform})")
        self.stdout.write(f"  * Working Directory: {os.getcwd()}")

        # Email 1 Settings
        e1_host = getattr(settings, 'EMAIL1_HOST', 'mail.uniquetechcamp.org')
        e1_port = getattr(settings, 'EMAIL1_PORT', 465)
        e1_ssl  = getattr(settings, 'EMAIL1_USE_SSL', True)
        e1_tls  = getattr(settings, 'EMAIL1_USE_TLS', False)
        e1_user = getattr(settings, 'EMAIL1_HOST_USER', 'info@uniquetechcamp.org')
        self.stdout.write(f"\n  Email 1 (Primary cPanel):")
        self.stdout.write(f"    Host/Port : {e1_host}:{e1_port} (SSL={e1_ssl}, TLS={e1_tls})")
        self.stdout.write(f"    Username  : {e1_user}")

        # Email 2 Settings
        e2_host = getattr(settings, 'EMAIL2_HOST', 'smtp.gmail.com')
        e2_port = getattr(settings, 'EMAIL2_PORT', 465)
        e2_ssl  = getattr(settings, 'EMAIL2_USE_SSL', True)
        e2_tls  = getattr(settings, 'EMAIL2_USE_TLS', False)
        e2_user = getattr(settings, 'EMAIL2_HOST_USER', 'UniqueTechCamp@gmail.com')
        raw_pwd = getattr(settings, 'EMAIL2_HOST_PASSWORD', '')
        clean_pwd = str(raw_pwd).replace(' ', '').strip().strip('"').strip("'")
        masked_pwd = (clean_pwd[:2] + '*' * (len(clean_pwd) - 4) + clean_pwd[-2:]) if len(clean_pwd) >= 4 else '****'

        self.stdout.write(f"\n  Email 2 (Google App Password Alternative):")
        self.stdout.write(f"    Host/Port : {e2_host}:{e2_port} (SSL={e2_ssl}, TLS={e2_tls})")
        self.stdout.write(f"    Username  : {e2_user}")
        self.stdout.write(f"    Password  : {masked_pwd} (Length: {len(clean_pwd)} chars)")

        # ----------------------------------------------------------------------
        # 2. RAW TCP OUTBOUND SOCKET CONNECTIVITY (FIREWALL TEST)
        # ----------------------------------------------------------------------
        self.stdout.write(self.style.HTTP_INFO("\n[2] Testing Outbound Network & Port Accessibility (Firewall Check):"))
        targets = [
            ("smtp.gmail.com", 465, "Google SMTP (SSL)"),
            ("smtp.gmail.com", 587, "Google SMTP (STARTTLS)"),
            ("mail.uniquetechcamp.org", 465, "cPanel Mail (SSL)"),
        ]

        socket_results = {}
        for host, port, desc in targets:
            start_t = timezone.now()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(6.0)
            try:
                s.connect((host, port))
                elapsed_ms = (timezone.now() - start_t).total_seconds() * 1000
                self.stdout.write(self.style.SUCCESS(f"  [OK]   {desc} -> {host}:{port} CONNECTED in {elapsed_ms:.1f}ms"))
                socket_results[(host, port)] = True
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  [FAIL] {desc} -> {host}:{port} FAILED: {e}"))
                socket_results[(host, port)] = False
            finally:
                s.close()

        # ----------------------------------------------------------------------
        # 3. DIRECT RAW SMTP AUTHENTICATION TESTS
        # ----------------------------------------------------------------------
        self.stdout.write(self.style.HTTP_INFO("\n[3] Testing Raw Google SMTP Authentication with App Password:"))
        
        # Test Port 465 SSL
        self.stdout.write(f"  Testing smtp.gmail.com:465 with SSL...")
        try:
            context = ssl.create_default_context()
            server_465 = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=10)
            server_465.set_debuglevel(0)
            server_465.ehlo()
            auth_res = server_465.login(e2_user, clean_pwd)
            self.stdout.write(self.style.SUCCESS(f"  [OK]   Port 465 SSL Authenticated Successfully: {auth_res}"))
            server_465.quit()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  [FAIL] Port 465 SSL Authentication Failed: {type(e).__name__}: {e}"))

        # Test Port 587 TLS
        self.stdout.write(f"\n  Testing smtp.gmail.com:587 with STARTTLS...")
        try:
            server_587 = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server_587.set_debuglevel(0)
            server_587.ehlo()
            server_587.starttls()
            server_587.ehlo()
            auth_res = server_587.login(e2_user, clean_pwd)
            self.stdout.write(self.style.SUCCESS(f"  [OK]   Port 587 TLS Authenticated Successfully: {auth_res}"))
            server_587.quit()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  [FAIL] Port 587 TLS Authentication Failed: {type(e).__name__}: {e}"))

        # ----------------------------------------------------------------------
        # 4. DATABASE RECENT PRODUCTION EMAIL LOGS INSPECTION
        # ----------------------------------------------------------------------
        self.stdout.write(self.style.HTTP_INFO("\n[4] Inspecting Last 15 Production Email Logs from Database:"))
        try:
            recent_logs = EmailLog.objects.order_by('-id')[:15]
            if not recent_logs.exists():
                self.stdout.write("  (No email logs found in database yet)")
            else:
                failed_found = 0
                for log in recent_logs:
                    status_style = self.style.SUCCESS if log.status == 'sent' else (
                        self.style.ERROR if log.status == 'failed' else self.style.WARNING
                    )
                    self.stdout.write(
                        f"  Log #{log.id} [{log.created_at.strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"Sender: {log.sender_choice} | To: {log.to_email} | Status: "
                        + status_style(f"[{log.status.upper()}]")
                    )
                    if log.status == 'failed' and log.error_message:
                        failed_found += 1
                        self.stdout.write(self.style.ERROR(f"     >>> ERROR DETAIL: {log.error_message}"))
                
                if failed_found == 0:
                    self.stdout.write(self.style.SUCCESS("\n  [OK] No recent failed emails found in database!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  Could not read EmailLog from database: {e}"))

        # ----------------------------------------------------------------------
        # 5. OPTIONAL LIVE DISPATCH TEST
        # ----------------------------------------------------------------------
        test_target = options.get('send_to')
        if test_target:
            self.stdout.write(self.style.HTTP_INFO(f"\n[5] Executing Live Dispatch Test via Email 2 to {test_target}..."))
            success, log_entry = send_robust_email(
                to_email=test_target,
                subject="UniqueTechCamp Production Email Diagnostic Test",
                body_text="This is an automated verification test dispatched via Email 2 (Google App Password).",
                sender_choice='email2',
                recipient_name="Production Admin",
            )
            if success:
                self.stdout.write(self.style.SUCCESS(f"  [OK] Live test email sent successfully! Log ID: #{log_entry.id}"))
            else:
                self.stdout.write(self.style.ERROR(f"  [FAIL] Live test email failed! Error: {log_entry.error_message}"))

        self.stdout.write(self.style.NOTICE("\n" + "=" * 70))
        self.stdout.write(self.style.NOTICE("  DIAGNOSTICS COMPLETE"))
        self.stdout.write(self.style.NOTICE("=" * 70 + "\n"))
