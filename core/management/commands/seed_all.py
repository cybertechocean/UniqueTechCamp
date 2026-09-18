from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Master Seeder: Seeds all 165+ services, AI coding prompts, blog articles, and portfolio projects into production"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=================================================="))
        self.stdout.write(self.style.NOTICE(">> UNIQUE TECH CAMP -- MASTER PRODUCTION SEEDER"))
        self.stdout.write(self.style.NOTICE("=================================================="))

        # 1. Services (165+ services across 20 categories)
        self.stdout.write(self.style.HTTP_INFO("\n[1/4] Seeding 165+ Services & Systems..."))
        try:
            call_command('seed_services')
            self.stdout.write(self.style.SUCCESS("[OK] Services and categories seeded successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[FAIL] Failed seeding services: {e}"))

        # 2. AI Master Prompts & Categories
        self.stdout.write(self.style.HTTP_INFO("\n[2/4] Seeding AI Master Coding Prompts Catalog..."))
        try:
            call_command('seed_ai_prompts')
            self.stdout.write(self.style.SUCCESS("[OK] AI Master Coding Prompts seeded successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[FAIL] Failed seeding AI prompts: {e}"))

        # 3. Blog Articles & Categories
        self.stdout.write(self.style.HTTP_INFO("\n[3/4] Seeding Growth Insights & Blog Articles..."))
        try:
            call_command('seed_blog')
            self.stdout.write(self.style.SUCCESS("[OK] Blog articles and categories seeded successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[FAIL] Failed seeding blog: {e}"))

        # 4. Portfolio Projects & Case Studies
        self.stdout.write(self.style.HTTP_INFO("\n[4/4] Seeding Flagship Portfolio Projects & Case Studies..."))
        try:
            call_command('seed_portfolio')
            self.stdout.write(self.style.SUCCESS("[OK] Portfolio projects and case studies seeded successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"[FAIL] Failed seeding portfolio: {e}"))

        self.stdout.write(self.style.NOTICE("\n=================================================="))
        self.stdout.write(self.style.SUCCESS(">> MASTER SEEDING COMPLETE! All production content is live."))
        self.stdout.write(self.style.NOTICE("=================================================="))
