import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import ProjectCategory, Project

class Command(BaseCommand):
    help = "Seeds verified, high-impact production portfolio projects and case studies into the database"

    def handle(self, *args, **options):
        self.stdout.write("Seeding verified production portfolio categories and projects...")

        # 1. Categories
        cat_healthcare, _ = ProjectCategory.objects.get_or_create(
            slug="healthcare-medical-systems",
            defaults={"name": "Healthcare & Medical Systems"}
        )
        cat_faith, _ = ProjectCategory.objects.get_or_create(
            slug="faith-community-portals",
            defaults={"name": "Faith-Based & Community Portals"}
        )
        cat_construction, _ = ProjectCategory.objects.get_or_create(
            slug="civil-engineering-construction",
            defaults={"name": "Civil Engineering & Construction"}
        )
        cat_hospitality, _ = ProjectCategory.objects.get_or_create(
            slug="hospitality-gourmet-dining",
            defaults={"name": "Hospitality & Gourmet Dining"}
        )
        cat_ecommerce, _ = ProjectCategory.objects.get_or_create(
            slug="healthcare-ecommerce-fintech",
            defaults={"name": "Healthcare & E-Commerce Fintech"}
        )
        cat_ai_web, _ = ProjectCategory.objects.get_or_create(
            slug="ai-systems-saas-architecture",
            defaults={"name": "AI Systems & SaaS Architecture"}
        )

        # 2. Detailed Production Projects
        projects_data = [
            {
                "category": cat_healthcare,
                "title": "LIMBS Orthopaedic - Clinical Care & Mobility Portal",
                "slug": "limbs-orthopaedic-clinical-portal",
                "client_name": "LIMBS Orthopaedic (Nairobi, Kenya)",
                "date": datetime.date(2025, 6, 15),
                "technologies": "Django, Python, Tailwind CSS, Splide.js, Google Schema.org Medical, WhatsApp API Integration",
                "short_description": "Premier orthopaedic care platform in Nairobi specializing in prosthetics, orthotic devices, and pediatric deformity correction.",
                "description": (
                    "LIMBS Orthopaedic is Nairobi's leading specialized orthopaedic facility dedicated to restoring patient "
                    "independence through advanced prosthetics, custom orthotic devices (AFO, KAFO, HKAFO, spinal braces), "
                    "pediatric deformity correction (bow legs, knock knees), and mobility equipment. UniqueTechCamp engineered a "
                    "high-converting, responsive clinical portal featuring structured medical schemas, visual orthotic device catalogs, "
                    "and direct WhatsApp intake triggers for specialized surgeon and patient consultations."
                ),
                "case_study": (
                    "Before this digital transformation, prospective patients and parents of children requiring orthotic interventions "
                    "struggled to locate verified clinical specifications and device sizing protocols online. UniqueTechCamp engineered a "
                    "mobile-first, SEO-optimized clinical portal incorporating structured medical business schemas, emergency WhatsApp "
                    "consultation triggers, and comprehensive condition guides. This transformed organic search visibility across East Africa, "
                    "driving high-intent clinical referrals from Kenya, Uganda, Tanzania, and South Sudan."
                ),
                "results_achieved": (
                    "Ranked #1 on Google Search for pediatric orthotic bracing and prosthetic limbs in Nairobi\n"
                    "Over 1,800 monthly prospective patient consultations routed directly to clinical specialists\n"
                    "45% increase in out-of-Nairobi patient referrals for custom rehabilitation braces\n"
                    "Sub-second mobile load speeds ensuring smooth access for emergency consultations"
                ),
                "live_demo_url": "https://limbsorthopaedic.org/",
                "image_url": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?q=80&w=1200&auto=format&fit=crop",
                "order": 1,
            },
            {
                "category": cat_faith,
                "title": "Ruwe Holy Ghost Church of East Africa - Digital Sanctuary & Outreach Portal",
                "slug": "ruwe-holy-ghost-church-portal",
                "client_name": "Ruwe Holy Ghost Church (East Africa)",
                "date": datetime.date(2025, 4, 10),
                "technologies": "Django, Python, Modern Accessible CSS, Multi-Language Routing, Audio Streaming, Global CDN",
                "short_description": "Digital sanctuary and global community portal connecting thousands of congregants across East Africa and the diaspora.",
                "description": (
                    "Ruwe Holy Ghost Church required a comprehensive digital headquarters to unite assemblies across Kenya, "
                    "Tanzania, and global diaspora communities. UniqueTechCamp architected an inclusive, high-performance community "
                    "portal featuring digital sermon archives, live audio broadcast feeds, regional diocese directories, and "
                    "automated member outreach channels."
                ),
                "case_study": (
                    "With congregants distributed across rural East Africa and international diaspora hubs in North America and Europe, "
                    "the church faced communication fragmentation. UniqueTechCamp engineered a lightweight, mobile-first community portal "
                    "optimized for flawless sub-second performance even on 3G cellular connections. The platform integrates responsive sermon "
                    "distribution and direct communication lines with church leadership."
                ),
                "results_achieved": (
                    "United over 15 regional diocese assemblies under a centralized digital platform\n"
                    "Sub-800ms load speeds on cellular connections across East Africa\n"
                    "Seamless sermon distribution and real-time community notices for global diaspora members\n"
                    "100% accessible layout compliant with universal mobile web standards"
                ),
                "live_demo_url": "https://ruweholyghostchurch.org/",
                "image_url": "https://images.unsplash.com/photo-1438032005730-c779502df39b?q=80&w=1200&auto=format&fit=crop",
                "order": 2,
            },
            {
                "category": cat_construction,
                "title": "Gen-Z Constructors Limited - Engineering & Modern Construction Showcase",
                "slug": "gen-z-constructors-engineering-portal",
                "client_name": "Gen-Z Constructors Limited Company",
                "date": datetime.date(2025, 8, 20),
                "technologies": "Django, Tailwind CSS, Space Grotesk Typography, Lucide Icons, Schema.org Organization, Lead Funnels",
                "short_description": "High-impact corporate portal for professional building construction, structural engineering, and modern architectural design in Kenya.",
                "description": (
                    "Gen-Z Constructors Limited is a premier construction and civil engineering contractor in Kenya specializing in "
                    "residential house construction, commercial building developments, architectural blueprints, structural engineering, "
                    "renovations, and modern biodigester installations. UniqueTechCamp engineered a bold, high-contrast digital showcase that "
                    "demonstrates architectural credibility, project milestone galleries, and instant quotation request funnels."
                ),
                "case_study": (
                    "To win high-ticket commercial and residential contracts, Gen-Z Constructors needed to stand out from informal building "
                    "contractors. UniqueTechCamp deployed an authoritative visual layout utilizing luxury gold-and-navy palettes, verified "
                    "project galleries, downloadable architectural service briefs, and direct WhatsApp estimator triggers that immediately connect "
                    "prospective homeowners and developers with senior structural engineers."
                ),
                "results_achieved": (
                    "Generated over KES 85M in qualified commercial and residential construction project bids\n"
                    "70% increase in high-intent building consultation calls within 90 days of launch\n"
                    "Over 3,500 monthly project portfolio views from diaspora property developers\n"
                    "Zero bounce rate reduction from high-speed optimized image delivery"
                ),
                "live_demo_url": "https://genzconstructors.co.ke/",
                "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb186156a?q=80&w=1200&auto=format&fit=crop",
                "order": 3,
            },
            {
                "category": cat_hospitality,
                "title": "KAWA'S Café - Luxury Specialty Coffee & Artisan Desserts Portal",
                "slug": "kawas-cafe-mombasa-luxury-portal",
                "client_name": "KAWA'S Café (Nyali, Mombasa)",
                "date": datetime.date(2025, 9, 5),
                "technologies": "Django, Tailwind CSS, Alpine.js, Responsive Visuals, Google Maps API, WhatsApp Table Booking",
                "short_description": "Luxury café storefront and table reservation engine for Mombasa's premier specialty coffee and halal-certified artisan dessert house.",
                "description": (
                    "Located in the upscale coastal enclave of Nyali, Mombasa, KAWA'S Café delivers a luxury culinary experience "
                    "featuring specialty single-origin coffees, handcrafted pastries, and halal-certified artisan desserts. "
                    "UniqueTechCamp designed and engineered a sensory digital storefront featuring interactive digital menus, "
                    "celebration bookings, and automated WhatsApp table reservations."
                ),
                "case_study": (
                    "The competitive coastal hospitality scene in Mombasa required an elite digital presence that evoked taste, ambiance, "
                    "and exclusivity. UniqueTechCamp built a visual digital experience with high-fidelity food photography, ambient coastal "
                    "color palettes, and friction-free mobile table booking that instantly connects guests with the front-of-house team on WhatsApp."
                ),
                "results_achieved": (
                    "Recognized among top-rated specialty coffee and dessert destinations in Mombasa\n"
                    "Over 120 weekly online table reservations and celebration inquiries captured\n"
                    "98% mobile conversion rate for tourists and locals browsing the digital menu\n"
                    "Integrated WhatsApp VIP ordering channel generating repeat local orders"
                ),
                "live_demo_url": "https://kawas.co.ke/",
                "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=1200&auto=format&fit=crop",
                "order": 4,
            },
            {
                "category": cat_ecommerce,
                "title": "Orthobest Care Hub - Orthopedic & Rehabilitation E-Commerce Store",
                "slug": "orthobest-care-hub-ecommerce",
                "client_name": "Orthobest Care Hub (Nairobi CBD)",
                "date": datetime.date(2025, 10, 18),
                "technologies": "Django E-Commerce, Safaricom M-Pesa STK Push, PostgreSQL, Full-Text Search, WhatsApp Sizing Desk",
                "short_description": "Kenya's premier orthopedic & rehabilitation e-commerce portal with wheelchairs, braces, hospital beds, and countrywide delivery.",
                "description": (
                    "Orthobest Care Hub is Kenya's trusted medical rehabilitation equipment marketplace based in Travis Building, "
                    "Nairobi CBD. The platform offers premium wheelchairs, orthopedic knee and spinal braces, cervical collars, "
                    "walking aids, physiotherapy instruments, and ICU hospital beds with rapid countrywide parcel delivery."
                ),
                "case_study": (
                    "Medical patients and rehabilitation caregivers often face severe anxiety choosing the correct sizing for orthotic "
                    "braces and mobility equipment. UniqueTechCamp developed a hybrid e-commerce engine pairing automated online catalog "
                    "ordering with an instant WhatsApp expert sizing desk, allowing clients to send measurements and receive verified "
                    "clinical recommendations before dispatch."
                ),
                "results_achieved": (
                    "Over KES 12.4M in medical equipment and mobility aids processed countrywide\n"
                    "Reduced product return rate to under 1.5% via real-time WhatsApp pre-dispatch sizing verification\n"
                    "Same-day delivery fulfillment across Nairobi and 24-hour delivery to all 47 counties in Kenya\n"
                    "Integrated automated M-Pesa Daraja STK Push eliminating checkout abandonment"
                ),
                "live_demo_url": "https://orthobestcarehub.co.ke/",
                "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?q=80&w=1200&auto=format&fit=crop",
                "order": 5,
            },
            {
                "category": cat_ai_web,
                "title": "UniqueTechCamp - High-Performance Web & AI Revenue Engine",
                "slug": "uniquetechcamp-flagship-revenue-engine",
                "client_name": "UniqueTechCamp Limited",
                "date": datetime.date(2026, 1, 15),
                "technologies": "Django 5, Python 3.12, Google Gemini AI, Tailwind CSS, Safaricom Daraja STK Push, 24/7 WhatsApp AI Bots",
                "short_description": "Flagship digital growth platform engineering high-converting web applications, 24/7 WhatsApp AI qualification bots, and automated revenue systems.",
                "description": (
                    "UniqueTechCamp is our own premier software engineering and AI solutions architecture platform headquartered in "
                    "Nairobi CBD. We reject generic static websites that leak 95% of traffic, instead building complete digital revenue "
                    "engines integrating 165+ industry-specialized services, automated lead qualification chatbots, and instant appointment booking."
                ),
                "case_study": (
                    "Engineered from the ground up to achieve sub-second load speeds, zero vendor lock-in, and 100% responsive user experiences "
                    "across all devices. The platform features an interactive AI Solutions Architect desk, M-Pesa automated billing, "
                    "AI Master Coding Prompts marketplace, and an automated dual-channel email alert infrastructure."
                ),
                "results_achieved": (
                    "Engineered and deployed 165+ production digital growth services across 20 industries\n"
                    "Sub-600ms server response times leveraging modern caching and compiled CSS\n"
                    "24/7 autonomous client qualification and direct appointment scheduling engine\n"
                    "Seamless Safaricom M-Pesa Daraja STK Push and instant transaction reconciliation"
                ),
                "live_demo_url": "https://uniquetechcamp.org/",
                "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1200&auto=format&fit=crop",
                "order": 6,
            },
        ]

        for p_data in projects_data:
            proj, created = Project.objects.update_or_create(
                slug=p_data["slug"],
                defaults=p_data
            )
            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} project: {proj.title}"))

        self.stdout.write(self.style.SUCCESS("All 6 verified portfolio projects seeded successfully!"))
