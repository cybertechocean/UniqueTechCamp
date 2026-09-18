import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import ProjectCategory, Project

class Command(BaseCommand):
    help = "Seeds initial high-converting portfolio projects and case studies"

    def handle(self, *args, **options):
        self.stdout.write("Seeding portfolio categories and projects...")

        cat_health, _ = ProjectCategory.objects.get_or_create(
            slug="healthcare-systems",
            defaults={"name": "Healthcare & Clinics"}
        )
        cat_ecom, _ = ProjectCategory.objects.get_or_create(
            slug="ecommerce-fintech",
            defaults={"name": "E-Commerce & Fintech"}
        )
        cat_tours, _ = ProjectCategory.objects.get_or_create(
            slug="travel-hospitality",
            defaults={"name": "Travel & Hospitality"}
        )
        cat_realestate, _ = ProjectCategory.objects.get_or_create(
            slug="real-estate-property",
            defaults={"name": "Real Estate & Property"}
        )
        cat_ai, _ = ProjectCategory.objects.get_or_create(
            slug="ai-automation-bots",
            defaults={"name": "AI Systems & WhatsApp Bots"}
        )

        projects_data = [
            {
                "category": cat_health,
                "title": "AfyaCore Diagnostic Clinic & Healthcare Portal",
                "slug": "afyacore-clinic-management-portal",
                "client_name": "AfyaCore Medical Care (Nairobi)",
                "technologies": "Django, PostgreSQL, Tailwind CSS, Safaricom M-Pesa Daraja API, WhatsApp Cloud API",
                "short_description": "Automated outpatient booking, electronic medical records (EMR), and automated M-Pesa billing.",
                "description": "AfyaCore needed to modernize their busy outpatient clinic in Nairobi, where patient wait times averaged over 75 minutes and manual paper billing created cash reconciliation discrepancies. UniqueTechCamp engineered a complete cloud healthcare portal featuring doctor schedule management, 24/7 patient booking via Web and WhatsApp, and automated M-Pesa STK Push checkouts.",
                "case_study": "By deploying an end-to-end appointment intake workflow, AfyaCore reduced patient waiting room congestion by 65%. Automated WhatsApp appointment reminders dispatched 24 hours and 2 hours prior reduced clinic no-shows to under 4%.",
                "results_achieved": "65% reduction in patient check-in wait times\nZero cash reconciliation discrepancies via automated M-Pesa Daraja reconciliation\nOver 2,400 outpatient appointments booked in the first 90 days",
                "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?q=80&w=1200&auto=format&fit=crop",
                "order": 1,
            },
            {
                "category": cat_ecom,
                "title": "ZenoCommerce Modern Storefront & M-Pesa STK Push Engine",
                "slug": "zenocommerce-mpesa-ecommerce-storefront",
                "client_name": "Zeno Retail Group Kenya",
                "technologies": "Python, Django, Redis Caching, Safaricom Daraja STK Push, Tailwind CSS",
                "short_description": "Sub-second digital storefront with 1-click M-Pesa Daraja STK Push and live parcel tracking.",
                "description": "Zeno Retail was struggling with a slow, bloated WooCommerce storefront that suffered from an 8.4-second page load time and high checkout abandonment. UniqueTechCamp re-engineered the storefront on a ultra-fast Django core with sub-600ms load speeds, direct Safaricom M-Pesa STK Push, and automated SMS order confirmation.",
                "case_study": "Migrating from WordPress to our custom architecture increased overall conversion rate from 1.2% to 4.8%. Mobile customers now complete transactions in under 20 seconds using native M-Pesa STK Push without copying till numbers.",
                "results_achieved": "4x increase in mobile checkout completion rate\nSub-600ms page load speeds across all product categories\nProcessed over KES 18.5M in automated transactions within 6 months",
                "image_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?q=80&w=1200&auto=format&fit=crop",
                "order": 2,
            },
            {
                "category": cat_ai,
                "title": "Autonomous 24/7 WhatsApp Lead Qualification Bot for B2B Services",
                "slug": "b2b-whatsapp-ai-lead-qualification-agent",
                "client_name": "PrimeGate Logistics & Freight",
                "technologies": "WhatsApp Business Cloud API, Google Gemini AI, Python, Webhooks, Google Sheets Sync",
                "short_description": "24/7 bilingual qualification agent that screens cargo inquiries, quotes pricing, and books consultations.",
                "description": "PrimeGate received hundreds of inbound WhatsApp inquiries daily for cross-border haulage and customs clearance. Sales representatives spent 4+ hours daily answering repetitive FAQs. UniqueTechCamp deployed an intelligent conversational AI agent that screens cargo volume, destination, and urgency before routing hot leads to account managers.",
                "case_study": "The bot operates around the clock, qualifying prospective shippers in both English and Swahili. It generates itemized quotation estimates and logs leads into Google Sheets and CRM in real time.",
                "results_achieved": "100% instant reply rate under 10 seconds, 24/7/365\nOver 380 qualified freight leads captured monthly\nFreed up 22 hours per week for sales representatives to focus on enterprise closings",
                "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop",
                "order": 3,
            },
            {
                "category": cat_tours,
                "title": "SafariLuxe East Africa Expeditions & Custom Itinerary Builder",
                "slug": "safariluxe-tours-itinerary-booking-engine",
                "client_name": "SafariLuxe Wilderness Expeditions",
                "technologies": "Django, Alpine.js, Tailwind CSS, Stripe & Pesapal Integration, Google Maps API",
                "short_description": "Interactive safari itinerary builder, lodge availability engine, and multi-currency deposit checkout.",
                "description": "SafariLuxe needed a high-ticket digital presence capable of converting affluent international travelers from the US, UK, and Europe. UniqueTechCamp engineered a bespoke safari portal with an interactive itinerary creator, high-resolution lodge visualizers, and secure deposit processing in USD and EUR.",
                "case_study": "International organic search traffic increased by 310% following technical SEO and schema optimizations. Direct bookings without third-party OTA commissions increased by 42%.",
                "results_achieved": "42% increase in direct commission-free safari bookings\n310% growth in qualified international organic search traffic\nZero downtime during peak high-season migration booking periods",
                "image_url": "https://images.unsplash.com/photo-1516426122078-c23e76319801?q=80&w=1200&auto=format&fit=crop",
                "order": 4,
            },
            {
                "category": cat_realestate,
                "title": "PrimeHaven Commercial Property Deal Flow & Buyer Portal",
                "slug": "primehaven-real-estate-deal-portal",
                "client_name": "PrimeHaven Realty Ltd",
                "technologies": "Django, Leaflet Maps, WhatsApp Lead Funnel, AWS S3, Tailwind CSS",
                "short_description": "High-intent property showcase, virtual walkthroughs, and automated buyer financial qualification.",
                "description": "PrimeHaven required an elite web portal to market prime commercial developments and luxury residential apartments in Kilimani, Westlands, and Karen. UniqueTechCamp engineered a high-converting property showcase with virtual tours, interactive floor plans, and automated financial pre-qualification.",
                "case_study": "Prospective buyers complete an automated qualification intake that assesses cash vs. mortgage capability before scheduling private property viewings directly with lead brokers.",
                "results_achieved": "Over KES 140M in property deal pipeline generated\n82% of viewing requests pre-qualified with verified financing capacity\n5-star client satisfaction rating from international diaspora investors",
                "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1200&auto=format&fit=crop",
                "order": 5,
            }
        ]

        for p_data in projects_data:
            proj, created = Project.objects.update_or_create(
                slug=p_data["slug"],
                defaults=p_data
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} project: {proj.title}"))

        self.stdout.write(self.style.SUCCESS("All portfolio projects seeded successfully!"))
