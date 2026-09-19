import sys
from django.core.management.base import BaseCommand
from django.db import close_old_connections
from marketing.models import BulkCampaign
from marketing.dispatcher import dispatch_next_campaign_recipient, execute_campaign

class Command(BaseCommand):
    help = "Dispatches emails for a marketing campaign. Suitable for cPanel cron jobs or SSH terminal runs."

    def add_arguments(self, parser):
        parser.add_argument(
            '--campaign-id',
            type=int,
            help="Specific BulkCampaign ID (primary key) to process",
            default=None
        )
        parser.add_argument(
            '--step',
            action='store_true',
            help="Dispatch only a single next pending recipient instead of looping",
            default=False
        )
        parser.add_argument(
            '--all-pending',
            action='store_true',
            help="Process all campaigns currently marked as 'sending' or 'draft' with pending recipients",
            default=False
        )

    def handle(self, *args, **options):
        campaign_id = options.get('campaign_id')
        single_step = options.get('step')
        all_pending = options.get('all_pending')

        if not campaign_id and not all_pending:
            self.stdout.write(self.style.ERROR("Error: Please provide --campaign-id=<ID> or --all-pending."))
            sys.exit(1)

        close_old_connections()

        if campaign_id:
            try:
                campaign = BulkCampaign.objects.get(id=campaign_id)
            except BulkCampaign.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Campaign with ID {campaign_id} not found."))
                sys.exit(1)

            if single_step:
                self.stdout.write(f"Executing single dispatch step for Campaign {campaign.campaign_id}...")
                result = dispatch_next_campaign_recipient(campaign)
                if result.get('completed'):
                    self.stdout.write(self.style.SUCCESS(f"Campaign {campaign.campaign_id} finished! Sent: {result['sent_count']}, Failed: {result['failed_count']}"))
                else:
                    status = result.get('recipient_status')
                    style = self.style.SUCCESS if status == 'sent' else self.style.ERROR
                    self.stdout.write(style(f"Recipient {result.get('recipient_email')}: [{status.upper()}] | Remaining: {result.get('remaining_count')}"))
            else:
                self.stdout.write(f"Executing full campaign dispatch for {campaign.campaign_id} ({campaign.title})...")
                sent, failed = execute_campaign(campaign.id)
                self.stdout.write(self.style.SUCCESS(f"Campaign {campaign.campaign_id} complete. Total Sent: {sent}, Failed: {failed}"))

        elif all_pending:
            campaigns = BulkCampaign.objects.filter(status='sending')
            self.stdout.write(f"Found {campaigns.count()} campaigns currently marked as 'sending'.")
            for c in campaigns:
                self.stdout.write(f"Processing Campaign {c.campaign_id}...")
                sent, failed = execute_campaign(c.id)
                self.stdout.write(self.style.SUCCESS(f"Finished {c.campaign_id}: {sent} sent, {failed} failed."))
