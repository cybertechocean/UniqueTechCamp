import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import BulkCampaign, CampaignRecipient
from .utils import generate_excel_template, parse_spreadsheet
from .dispatcher import execute_campaign, send_test_email

class StaffOnlyMixin(UserPassesTestMixin):
    """Ensure only staff / administrators can access marketing & bulk emailing tools."""
    def test_func(self):
        # Allow staff members or superusers
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def handle_no_permission(self):
        messages.error(self.request, "Access restricted. You must be logged in as a UniqueTechCamp staff member to manage bulk email marketing.")
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
    """
    def get(self, request):
        campaigns = BulkCampaign.objects.all()[:20]
        total_campaigns = BulkCampaign.objects.count()
        total_recipients_reached = sum(c.sent_count for c in campaigns)

        context = {
            'campaigns': campaigns,
            'total_campaigns': total_campaigns,
            'total_recipients_reached': total_recipients_reached,
        }
        return render(request, 'marketing/dashboard.html', context)

    def post(self, request):
        title = request.POST.get('title', '').strip()
        sender_name = request.POST.get('sender_name', 'UniqueTechCamp Solutions').strip()
        sender_email = request.POST.get('sender_email', 'info@uniquetechcamp.org').strip()
        default_subject = request.POST.get('default_subject', '').strip()
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
            sender_name=sender_name,
            sender_email=sender_email,
            default_subject=default_subject,
            spreadsheet_file=spreadsheet_file,
            delay_seconds=delay_seconds,
            total_recipients=len(recipients_data),
            status='draft'
        )

        # Bulk Create Recipients
        recipient_objs = [
            CampaignRecipient(
                campaign=campaign,
                name=r['name'],
                email=r['email'],
                subject=r['subject'] or default_subject or title,
                personalized_message=r['message'],
                status='pending'
            )
            for r in recipients_data
        ]
        CampaignRecipient.objects.bulk_create(recipient_objs, batch_size=500)

        messages.success(request, f"Campaign '{campaign.title}' created with {len(recipient_objs)} recipients ready!")
        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignDetailView(StaffOnlyMixin, View):
    """
    Detailed campaign control room with live delivery status and test dispatch.
    """
    def get(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        filter_status = request.GET.get('status', '').strip()

        recipients = campaign.recipients.all()
        if filter_status in ('pending', 'sent', 'failed'):
            recipients = recipients.filter(status=filter_status)

        context = {
            'campaign': campaign,
            'recipients': recipients[:200], # Preview up to 200 rows in UI
            'filter_status': filter_status,
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
            messages.success(request, f"Test email successfully dispatched to {test_email}! Check your inbox to review formatting.")
        except Exception as e:
            messages.error(request, f"Error sending test email: {e}")

        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignStartSendingView(StaffOnlyMixin, View):
    """
    Triggers execution of the bulk sending campaign in a background worker thread.
    """
    def post(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)

        if campaign.status == 'sending':
            messages.warning(request, "Campaign is already actively in progress.")
            return redirect('marketing:campaign_detail', pk=campaign.id)

        # Launch dispatch thread
        dispatch_thread = threading.Thread(
            target=execute_campaign,
            args=(campaign.id,),
            daemon=True
        )
        dispatch_thread.start()

        messages.success(request, f"Campaign dispatch initiated! Emails will send with a {campaign.delay_seconds}s delay between each contact.")
        return redirect('marketing:campaign_detail', pk=campaign.id)


class CampaignStatusApiView(StaffOnlyMixin, View):
    """
    Instant JSON status endpoint for asynchronous dashboard polling.
    """
    def get(self, request, pk):
        campaign = get_object_or_404(BulkCampaign, pk=pk)
        return JsonResponse({
            'campaign_id': campaign.campaign_id,
            'status': campaign.status,
            'total_recipients': campaign.total_recipients,
            'sent_count': campaign.sent_count,
            'failed_count': campaign.failed_count,
            'progress_percentage': campaign.progress_percentage,
            'is_finished': campaign.is_finished,
        })
