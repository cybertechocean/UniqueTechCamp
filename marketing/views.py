import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import BulkCampaign, CampaignRecipient, EmailLog
from .utils import generate_excel_template, parse_spreadsheet
from .dispatcher import execute_campaign, send_test_email, dispatch_next_campaign_recipient
from .email_service import send_robust_email, get_sender_from_email

class StaffOnlyMixin(UserPassesTestMixin):
    """Ensure only staff / administrators can access marketing & bulk emailing tools."""
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def handle_no_permission(self):
        messages.error(self.request, "Access restricted. You must be logged in as a UniqueTechCamp staff member to access marketing and email operations.")
        return redirect('admin:login')


class DownloadTemplateView(View):
    """
    Download the official pre-formatted Excel (.xlsx) bulk emailing template.
    Includes columns: Full Name, Email Address, Subject Line, Personalized Message.
    """
    def get(self, request):
        excel_bytes = generate_excel_template()
        response = HttpResponse(
            excel_bytes,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="UniqueTechCamp_Bulk_Email_Template.xlsx"'
        return response


class CampaignDashboardView(StaffOnlyMixin, View):
    """
    Marketing Dashboard: Overview of all campaigns + Drag-and-drop spreadsheet uploader.
    Now with direct navigation to Send Single Email (/marketing/send-single/)
    and Centralized Email Logs (/marketing/emails-log/).
    """
    def get(self, request):
        campaigns = BulkCampaign.objects.all()[:20]
        total_campaigns = BulkCampaign.objects.count()
        total_recipients_reached = sum(c.sent_count for c in campaigns)
        
        # Email logs quick stats
        total_logs = EmailLog.objects.count()
        failed_logs = EmailLog.objects.filter(status='failed').count()

        context = {
            'campaigns': campaigns,
            'total_campaigns': total_campaigns,
            'total_recipients_reached': total_recipients_reached,
            'total_logs': total_logs,
            'failed_logs': failed_logs,
        }
        return render(request, 'marketing/dashboard.html', context)

    def post(self, request):
        title = request.POST.get('title', '').strip()
        sender_choice = request.POST.get('sender_choice', 'email1').strip()
        sender_name = request.POST.get('sender_name', 'UniqueTechCamp Solutions').strip()
        
        if sender_choice == 'email2':
            sender_email = 'UniqueTechCamp@gmail.com'
        else:
            sender_email = request.POST.get('sender_email', 'info@uniquetechcamp.org').strip()

        default_subject = request.POST.get('default_subject', '').strip()
        email_format = request.POST.get('email_format', 'branded').strip()
        delay_seconds = float(request.POST.get('delay_seconds', 2.0))
        spreadsheet_file = request.FILES.get('spreadsheet_file')

        if not title or not spreadsheet_file:
            messages.error(request, "Please provide a campaign title and upload an Excel (.xlsx) or CSV file.")
            return redirect('marketing:dashboard')

        # Parse file
        try:
            recipients_data = parse_spreadsheet(spreadsheet_file, default_subject=default_subject)
        except Exception as e:
            messages.error(request, f"Error parsing spreadsheet file: {e}. Please use the official downloadable template.")
            return redirect('marketing:dashboard')

        if not recipients_data:
            messages.error(request, "No valid email records were found in the uploaded file. Ensure column headers match the template.")
            return redirect('marketing:dashboard')

        # Create Campaign
        campaign = BulkCampaign.objects.create(
            title=title,
            sender_choice=sender_choice,
            sender_name=sender_name,
            sender_email=sender_email,
            default_subject=default_subject,
            email_format=email_format,
            spreadsheet_file=spreadsheet_file,
            delay_seconds=delay_seconds,
            total_recipients=len(recipients_data),
            status='draft'
        )

        # Bulk Create Recipients with Pre-Verification Details
        recipient_objs = [
            CampaignRecipient(
                campaign=campaign,
                name=r['name'],
                email=r['email'],
                subject=r['subject'] or default_subject or title,
                personalized_message=r['message'],
                status='pending',
                verification_status=r.get('verification_status', 'unverified'),
                verification_reason=r.get('verification_reason', ''),
                is_deliverable=r.get('is_deliverable', True),
            )
            for r in recipients_data
        ]
        CampaignRecipient.objects.bulk_create(recipient_objs, batch_size=500)

        verified_c = sum(1 for r in recipients_data if r.get('verification_status') == 'verified')
        invalid_c = sum(1 for r in recipients_data if r.get('verification_status') in ('invalid', 'suppressed'))

        if invalid_c > 0:
            messages.warning(
                request,
                f"Campaign '{campaign.title}' uploaded with {len(recipient_objs)} contacts: "
                f"{verified_c} clean & verified, {invalid_c} invalid/dead emails detected. "
                "Review or prune them in the Control Room before firing!"
            )
        else:
            messages.success(request, f"Campaign '{campaign.title}' created with {len(recipient_objs)} clean contacts ready!")

        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignDetailView(StaffOnlyMixin, View):
    """
    Detailed campaign control room with live delivery status, test dispatch,
    and Email Reputation Guardian deliverability shield.
    """
    def get(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        filter_status = request.GET.get('status', '').strip()
        filter_verification = request.GET.get('verification', '').strip()

        recipients = campaign.recipients.all()
        if filter_status in ('pending', 'sent', 'failed'):
            recipients = recipients.filter(status=filter_status)
        if filter_verification in ('verified', 'risky', 'invalid', 'suppressed', 'unverified'):
            recipients = recipients.filter(verification_status=filter_verification)

        verified_count = campaign.recipients.filter(verification_status='verified').count()
        risky_count = campaign.recipients.filter(verification_status='risky').count()
        invalid_count = campaign.recipients.filter(verification_status='invalid').count()
        suppressed_count = campaign.recipients.filter(verification_status='suppressed').count()

        context = {
            'campaign': campaign,
            'recipients': recipients[:200],
            'filter_status': filter_status,
            'filter_verification': filter_verification,
            'verified_count': verified_count,
            'risky_count': risky_count,
            'invalid_count': invalid_count,
            'suppressed_count': suppressed_count,
            'total_invalid_or_suppressed': invalid_count + suppressed_count,
            'default_test_email': request.user.email or 'UniqueTechCamp@gmail.com',
        }
        return render(request, 'marketing/detail.html', context)


class CampaignSendTestView(StaffOnlyMixin, View):
    """
    Dispatches a single test email preview to the admin/staff email.
    """
    def post(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        test_email = request.POST.get('test_email', '').strip()

        if not test_email or '@' not in test_email:
            messages.error(request, "Please enter a valid email address to receive the test broadcast.")
            return redirect('marketing:campaign_detail', pk=campaign.id)

        try:
            send_test_email(campaign, test_email)
            messages.success(request, f"Test email successfully dispatched to {test_email} via [{campaign.get_sender_choice_display()}]! Check your inbox.")
        except Exception as e:
            messages.error(request, f"Error sending test email: {e}")

        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignStartSendingView(StaffOnlyMixin, View):
    """
    Triggers execution of the bulk sending campaign.
    Supports both background thread dispatch and initiating the interactive browser runner.
    """
    def post(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)

        # Allow initiating interactive or background execution
        if campaign.status == 'sending' and not request.POST.get('force'):
            messages.warning(request, "Campaign is currently in progress. You can monitor live progress or click 'Reset to Draft' if stalled.")
            return redirect('marketing:campaign_detail', pk=campaign.id)

        # Mark campaign as sending
        campaign.status = 'sending'
        campaign.save(update_fields=['status'])

        # Start thread execution (for users who navigate away or use non-interactive mode)
        dispatch_thread = threading.Thread(
            target=execute_campaign,
            args=(campaign.id,),
            daemon=True
        )
        dispatch_thread.start()

        messages.success(request, f"Campaign dispatch initiated via [{campaign.get_sender_choice_display()}]! Emails are sending with a {campaign.delay_seconds}s delay.")
        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignDispatchStepApiView(StaffOnlyMixin, View):
    """
    Step-by-step interactive dispatch API endpoint.
    Called by the front-end browser runner to dispatch 1 recipient at a time.
    100% resilient to Phusion Passenger / WSGI request timeouts and thread terminations!
    """
    def post(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        result = dispatch_next_campaign_recipient(campaign)
        return JsonResponse(result)


class CampaignResetStatusView(StaffOnlyMixin, View):
    """
    Force-unlocks and resets a stalled or stuck campaign back to 'draft'
    (or 'completed' if all recipients have already been sent/failed).
    Accurately recalculates sent_count, failed_count, and remaining recipients.
    """
    def post(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        
        sent_c = campaign.recipients.filter(status='sent').count()
        failed_c = campaign.recipients.filter(status='failed').count()
        pending_c = campaign.recipients.filter(status='pending').count()

        campaign.sent_count = sent_c
        campaign.failed_count = failed_c
        
        if pending_c == 0 and (sent_c + failed_c) > 0:
            campaign.status = 'completed'
            if not campaign.completed_at:
                campaign.completed_at = timezone.now()
            status_msg = "All contacts already sent/failed. Campaign marked as Completed."
        else:
            campaign.status = 'draft'
            status_msg = f"Campaign unlocked and reset to Draft ({sent_c} sent, {failed_c} failed, {pending_c} pending remaining). You can now safely dispatch."

        campaign.save()
        messages.success(request, f"Campaign {campaign.campaign_id}: {status_msg}")
        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignStatusApiView(StaffOnlyMixin, View):
    """
    Instant JSON status endpoint for asynchronous dashboard polling.
    """
    def get(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        pending_count = campaign.recipients.filter(status='pending').count()
        return JsonResponse({
            'campaign_id': campaign.campaign_id,
            'status': campaign.status,
            'total_recipients': campaign.total_recipients,
            'sent_count': campaign.sent_count,
            'failed_count': campaign.failed_count,
            'pending_count': pending_count,
            'progress_percentage': campaign.progress_percentage,
            'is_finished': campaign.is_finished,
            'delay_seconds': campaign.delay_seconds,
        })


class CampaignValidateContactsView(StaffOnlyMixin, View):
    """
    Scans and verifies all pending contacts in a campaign using the Reputation Guardian.
    Validates DNS MX records, syntax, typos, disposable domains, and suppression list.
    """
    def post(self, request, pk):
        from .validator import verify_email_deliverability
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        pending = campaign.recipients.filter(status='pending')

        verified_c = 0
        risky_c = 0
        invalid_c = 0
        suppressed_c = 0

        for r in pending:
            res = verify_email_deliverability(r.email, check_dns=True, check_suppression=True)
            r.verification_status = res['status']
            r.verification_reason = res['reason']
            r.is_deliverable = res['is_safe']
            if res.get('was_fixed') and res.get('cleaned_email'):
                r.email = res['cleaned_email']
            r.save(update_fields=['verification_status', 'verification_reason', 'is_deliverable', 'email'])

            if res['status'] == 'verified':
                verified_c += 1
            elif res['status'] == 'risky':
                risky_c += 1
            elif res['status'] == 'suppressed':
                suppressed_c += 1
            else:
                invalid_c += 1

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.headers.get('accept', ''):
            return JsonResponse({
                'success': True,
                'verified_count': verified_c,
                'risky_count': risky_c,
                'invalid_count': invalid_c,
                'suppressed_count': suppressed_c,
                'total_checked': pending.count(),
            })

        messages.success(
            request,
            f"Reputation Shield Scan Complete: {verified_c} verified clean, {risky_c} risky, {invalid_c + suppressed_c} invalid/suppressed flagged."
        )
        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignPruneInvalidView(StaffOnlyMixin, View):
    """
    Prunes/removes invalid, dead domain, and suppressed contacts from the campaign queue.
    Ensures only verified and deliverable emails remain before bulk sending to protect sender score.
    """
    def post(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        invalid_recipients = campaign.recipients.filter(
            status='pending'
        ).filter(
            Q(verification_status__in=['invalid', 'suppressed']) | Q(is_deliverable=False)
        )
        count = invalid_recipients.count()
        invalid_recipients.delete()

        campaign.total_recipients = campaign.recipients.count()
        campaign.save(update_fields=['total_recipients'])

        messages.success(request, f"Cleaned campaign queue! Pruned {count} invalid/dead contacts. Sender reputation protected.")
        return redirect('marketing:campaign_detail', pk=campaign.id)


# ==============================================================================
# SINGLE / CUSTOM EMAIL VIEWS (WITH ATTACHMENTS & DUAL SENDER)
# ==============================================================================

class SendSingleEmailView(StaffOnlyMixin, View):
    """
    Ultra-Modern Single / Custom Email Composer.
    Supports:
    - Dual Senders (Email 1: info@uniquetechcamp.org vs Email 2: UniqueTechCamp@gmail.com)
    - Branded UTC layout or Welcome template preset
    - File attachments (PDF, DOCX, images, etc.)
    - Direct logging to EmailLog with error capture
    """
    def get(self, request):
        sender_choice = request.GET.get('sender', 'email1')
        to_email = request.GET.get('to_email', '')
        recipient_name = request.GET.get('name', '')
        subject = request.GET.get('subject', '')
        preset = request.GET.get('preset', 'branded')

        context = {
            'sender_choice': sender_choice,
            'to_email': to_email,
            'recipient_name': recipient_name,
            'subject': subject,
            'preset': preset,
            'sender_choices': EmailLog.SENDER_CHOICES,
        }
        return render(request, 'marketing/send_single.html', context)

    def post(self, request):
        sender_choice = request.POST.get('sender_choice', 'email1').strip()
        to_email = request.POST.get('to_email', '').strip()
        recipient_name = request.POST.get('recipient_name', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_body = request.POST.get('message', '').strip()
        email_format = request.POST.get('email_format', 'branded').strip()
        cta_text = request.POST.get('cta_text', '').strip()
        cta_url = request.POST.get('cta_url', '').strip()
        attachment = request.FILES.get('attachment')

        if not to_email or '@' not in to_email:
            messages.error(request, "Please provide a valid recipient email address.")
            return render(request, 'marketing/send_single.html', {
                'sender_choice': sender_choice, 'to_email': to_email,
                'recipient_name': recipient_name, 'subject': subject,
                'message': message_body, 'email_format': email_format,
                'cta_text': cta_text, 'cta_url': cta_url,
                'sender_choices': EmailLog.SENDER_CHOICES,
            })

        if not subject or not message_body:
            messages.error(request, "Please provide both an email subject line and message content.")
            return render(request, 'marketing/send_single.html', {
                'sender_choice': sender_choice, 'to_email': to_email,
                'recipient_name': recipient_name, 'subject': subject,
                'message': message_body, 'email_format': email_format,
                'cta_text': cta_text, 'cta_url': cta_url,
                'sender_choices': EmailLog.SENDER_CHOICES,
            })

        # Render HTML body depending on format
        email_type = 'single'
        if email_format == 'welcome':
            email_type = 'welcome'
            context = {
                'user_name': recipient_name or 'Valued Client',
                'cta_url': cta_url or 'https://uniquetechcamp.org/services/',
                'cta_text': cta_text or 'Explore 107 Growth Services →',
                'site_url': 'https://uniquetechcamp.org',
                'logo_url': 'https://uniquetechcamp.org/static/images/logo-rounded.png',
            }
            html_body = render_to_string('emails/welcome_email.html', context)
        elif email_format == 'branded':
            context = {
                'subject': subject,
                'recipient_name': recipient_name,
                'message': message_body,
                'cta_text': cta_text,
                'cta_url': cta_url,
                'site_url': 'https://uniquetechcamp.org',
                'logo_url': 'https://uniquetechcamp.org/static/images/logo-rounded.png',
            }
            html_body = render_to_string('emails/single_custom_email.html', context)
        else:
            # Plain text
            html_body = None

        # Dispatch via robust centralized service
        success, email_log = send_robust_email(
            to_email=to_email,
            subject=subject,
            body_text=message_body,
            body_html=html_body,
            sender_choice=sender_choice,
            recipient_name=recipient_name,
            attachment_file=attachment,
            attachment_filename=attachment.name if attachment else '',
            email_type=email_type,
        )

        if success:
            messages.success(request, f"Email successfully dispatched to {to_email} via {email_log.get_sender_choice_display()}!")
        else:
            messages.error(request, f"Email delivery to {to_email} failed: {email_log.error_message}. You can inspect and resend from Email Logs.")

        return redirect('marketing:emails_log')


# ==============================================================================
# CENTRALIZED EMAIL LOGS VIEWS (/marketing/emails-log/)
# ==============================================================================

class EmailLogListView(StaffOnlyMixin, View):
    """
    Centralized Email Logs Dashboard.
    Provides complete visibility over all outgoing emails:
    - Status filtering (All, Failed, Sent, Pending)
    - Sender filtering (Email 1 vs Email 2)
    - Type filtering (Single, Welcome, Campaign, Appointment, System)
    - Live search (Recipient, Subject, Error trace)
    - Quick actions: View details, 1-click Resend, Edit & Resend
    """
    def get(self, request):
        status_filter = request.GET.get('status', 'all').strip()
        sender_filter = request.GET.get('sender', 'all').strip()
        type_filter = request.GET.get('type', 'all').strip()
        query = request.GET.get('q', '').strip()

        logs = EmailLog.objects.all()

        # Global Counters
        total_count = logs.count()
        failed_count = EmailLog.objects.filter(status='failed').count()
        sent_count = EmailLog.objects.filter(status='sent').count()
        pending_count = EmailLog.objects.filter(status='pending').count()

        # Filter by status
        if status_filter in ('failed', 'sent', 'pending'):
            logs = logs.filter(status=status_filter)

        # Filter by sender
        if sender_filter in ('email1', 'email2'):
            logs = logs.filter(sender_choice=sender_filter)

        # Filter by type
        if type_filter in ('single', 'welcome', 'campaign', 'appointment', 'contact', 'system'):
            logs = logs.filter(email_type=type_filter)

        # Search
        if query:
            logs = logs.filter(
                Q(to_email__icontains=query) |
                Q(recipient_name__icontains=query) |
                Q(subject__icontains=query) |
                Q(error_message__icontains=query)
            )

        # Pagination: 25 logs per page
        paginator = Paginator(logs, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'logs': page_obj,
            'page_obj': page_obj,
            'status_filter': status_filter,
            'sender_filter': sender_filter,
            'type_filter': type_filter,
            'query': query,
            'total_count': total_count,
            'failed_count': failed_count,
            'sent_count': sent_count,
            'pending_count': pending_count,
            'sender_choices': EmailLog.SENDER_CHOICES,
            'type_choices': EmailLog.EMAIL_TYPE_CHOICES,
        }
        return render(request, 'marketing/emails_log.html', context)


class EmailLogResendView(StaffOnlyMixin, View):
    """
    1-Click Resend action for failed or pending emails.
    Allows specifying an alternative sender (e.g. switch from Email 1 to Email 2).
    """
    def post(self, request, pk):
        email_log = get_object_or_404(EmailLog, pk=pk)
        sender_choice = request.POST.get('sender_choice', email_log.sender_choice).strip()

        success, updated_log = send_robust_email(
            to_email=email_log.to_email,
            subject=email_log.subject,
            body_text=email_log.body_text,
            body_html=email_log.body_html,
            sender_choice=sender_choice,
            recipient_name=email_log.recipient_name,
            email_type=email_log.email_type,
            existing_log=email_log,
        )

        if success:
            messages.success(request, f"Successfully resent email to {email_log.to_email} via [{updated_log.get_sender_choice_display()}]!")
        else:
            messages.error(request, f"Resend failed: {updated_log.error_message}. You can edit details or switch senders before retrying.")

        # Support AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': success,
                'status': updated_log.status,
                'error_message': updated_log.error_message,
            })

        return redirect('marketing:emails_log')

    def get(self, request, pk):
        # Allow 1-click GET resend
        return self.post(request, pk)


class EmailLogEditView(StaffOnlyMixin, View):
    """
    View & Edit failed email prior to resending.
    Allows changing recipient, sender (Email 1 vs Email 2), subject, body, or replacing attachment.
    """
    def get(self, request, pk):
        email_log = get_object_or_404(EmailLog, pk=pk)
        context = {
            'email_log': email_log,
            'sender_choices': EmailLog.SENDER_CHOICES,
        }
        return render(request, 'marketing/email_edit.html', context)

    def post(self, request, pk):
        email_log = get_object_or_404(EmailLog, pk=pk)

        sender_choice = request.POST.get('sender_choice', email_log.sender_choice).strip()
        to_email = request.POST.get('to_email', email_log.to_email).strip()
        recipient_name = request.POST.get('recipient_name', email_log.recipient_name).strip()
        subject = request.POST.get('subject', email_log.subject).strip()
        body_text = request.POST.get('body_text', email_log.body_text).strip()
        attachment = request.FILES.get('attachment')

        if not to_email or not subject or not body_text:
            messages.error(request, "Recipient email, subject, and message are all required.")
            return redirect('marketing:email_edit', pk=pk)

        # Update and resend
        email_log.sender_choice = sender_choice
        email_log.to_email = to_email
        email_log.recipient_name = recipient_name
        email_log.subject = subject
        email_log.body_text = body_text

        # Re-wrap HTML if it was branded
        if email_log.email_type == 'single' or email_log.body_html:
            context = {
                'subject': subject,
                'recipient_name': recipient_name,
                'message': body_text,
                'site_url': 'https://uniquetechcamp.org',
                'logo_url': 'https://uniquetechcamp.org/static/images/logo-rounded.png',
            }
            email_log.body_html = render_to_string('emails/single_custom_email.html', context)

        success, updated_log = send_robust_email(
            to_email=to_email,
            subject=subject,
            body_text=body_text,
            body_html=email_log.body_html,
            sender_choice=sender_choice,
            recipient_name=recipient_name,
            attachment_file=attachment,
            attachment_filename=attachment.name if attachment else '',
            email_type=email_log.email_type,
            existing_log=email_log,
        )

        if success:
            messages.success(request, f"Email updated and successfully sent to {to_email} via [{updated_log.get_sender_choice_display()}]!")
        else:
            messages.error(request, f"Updated dispatch failed: {updated_log.error_message}")

        return redirect('marketing:emails_log')


class EmailLogDeleteView(StaffOnlyMixin, View):
    """
    Remove an individual log entry from the logs.
    """
    def post(self, request, pk):
        email_log = get_object_or_404(EmailLog, pk=pk)
        recipient = email_log.to_email
        email_log.delete()
        messages.success(request, f"Email log for {recipient} was removed.")
        return redirect('marketing:emails_log')


class ResendAllFailedEmailsView(StaffOnlyMixin, View):
    """
    Batch resend all currently failed emails with 1 click.
    Optionally allows routing all of them through Email 2 (Gmail App Password).
    """
    def post(self, request):
        sender_choice = request.POST.get('sender_choice', '').strip()
        failed_logs = EmailLog.objects.filter(status='failed')
        total_failed = failed_logs.count()

        if total_failed == 0:
            messages.info(request, "There are currently no failed emails in the log.")
            return redirect('marketing:emails_log')

        success_count = 0
        for log in failed_logs:
            choice = sender_choice or log.sender_choice
            success, _ = send_robust_email(
                to_email=log.to_email,
                subject=log.subject,
                body_text=log.body_text,
                body_html=log.body_html,
                sender_choice=choice,
                recipient_name=log.recipient_name,
                email_type=log.email_type,
                existing_log=log,
            )
            if success:
                success_count += 1

        messages.success(request, f"Batch resend completed! {success_count} of {total_failed} failed emails sent successfully.")
        return redirect('marketing:emails_log')


class SyncWelcomeLogsView(StaffOnlyMixin, View):
    """
    Inspects all registered users in the database.
    If any user with an email address has not had a successful welcome email logged,
    generates an EmailLog record marked as failed ('Previous welcome email was not confirmed sent')
    so that staff can immediately inspect, edit, or resend it with 1 click.
    """
    def post(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        users_with_email = User.objects.filter(email__isnull=False).exclude(email='')
        created_count = 0

        for u in users_with_email:
            already_logged = EmailLog.objects.filter(to_email__iexact=u.email.strip(), email_type='welcome').exists()
            if not already_logged:
                user_name = u.get_full_name() or u.username
                context = {
                    'user_name': user_name,
                    'cta_url': 'https://uniquetechcamp.org/services/',
                    'cta_text': 'Explore 107 Growth Services →',
                    'site_url': 'https://uniquetechcamp.org',
                    'logo_url': 'https://uniquetechcamp.org/static/images/logo-rounded.png',
                }
                html_body = render_to_string('emails/welcome_email.html', context)
                text_body = strip_tags(html_body)

                EmailLog.objects.create(
                    sender_choice='email1',
                    from_email='UniqueTechCamp Solutions <info@uniquetechcamp.org>',
                    to_email=u.email.strip(),
                    recipient_name=user_name,
                    subject="Welcome to UniqueTechCamp — Website, Clients, Income",
                    body_text=text_body,
                    body_html=html_body,
                    email_type='welcome',
                    status='failed',
                    error_message="Previous welcome email delivery was not confirmed. Ready to inspect, edit, or resend.",
                )
                created_count += 1

        if created_count > 0:
            messages.success(request, f"Scanned registered users: Found and logged {created_count} users who did not receive welcome emails. They are now listed below ready to resend!")
        else:
            messages.info(request, "Scanned registered users: All users already have logged welcome email records.")

        return redirect('marketing:emails_log')


