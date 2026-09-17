import os
import re
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from services.models import ServiceCategory, Service
from services.management.commands.new_services_data import NEW_CATEGORIES, NEW_SERVICES

class Command(BaseCommand):
    help = "Seed database with 160+ comprehensive services with AI Lead Generation, Qualification, and Automated Follow-Up"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Beginning services seeding..."))

        # Automatically ensure MySQL/MariaDB tables support 4-byte UTF-8 emojis (utf8mb4)
        from django.db import connection
        if connection.vendor == 'mysql':
            tables_to_convert = [
                'services_servicecategory',
                'services_service',
                'services_serviceimage',
                'services_servicefeature',
                'services_servicefaq'
            ]
            with connection.cursor() as cursor:
                try:
                    cursor.execute("ALTER DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Notice: Database-level charset alter skipped: {e}"))
                for tbl in tables_to_convert:
                    try:
                        cursor.execute(f"ALTER TABLE `{tbl}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                        self.stdout.write(self.style.SUCCESS(f"Converted table `{tbl}` to utf8mb4."))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Could not convert `{tbl}` to utf8mb4: {e}"))

        # Helper to sanitize 4-byte characters if database still does not support utf8mb4
        def safe_text(val):
            return val


        # Category metadata: 4 New Core Categories + 16 Industry Verticals = 20 Categories
        categories_data = NEW_CATEGORIES + [
            {"id": "05", "name": "Retail & Commerce", "slug": "retail-commerce", "icon": "🛒", "icon_name": "shopping_cart", "order": 5, "desc": "E-commerce and retail storefronts with AI customer capture and WhatsApp checkout."},
            {"id": "06", "name": "Healthcare & Medical", "slug": "healthcare", "icon": "🏥", "icon_name": "local_hospital", "order": 6, "desc": "Clinics and medical centers with patient intake bots and automated appointment booking."},
            {"id": "07", "name": "Hospitality & Food", "slug": "hospitality-food", "icon": "🍽️", "icon_name": "restaurant", "order": 7, "desc": "Restaurants, hotels, and cafes with online ordering and automated table reservation systems."},
            {"id": "08", "name": "Education & Academies", "slug": "education", "icon": "🎓", "icon_name": "school", "order": 8, "desc": "Schools and training institutes with student enrollment funnels and course catalogues."},
            {"id": "09", "name": "Religious Organizations", "slug": "religious-organizations", "icon": "⛪", "icon_name": "church", "order": 9, "desc": "Churches and ministries with livestreaming, donations, and automated member outreach."},
            {"id": "10", "name": "Professional & Legal Services", "slug": "professional-services", "icon": "💼", "icon_name": "business_center", "order": 10, "desc": "Law firms and consultancies with high-value client qualification funnels."},
            {"id": "11", "name": "Automotive & Transport", "slug": "automotive", "icon": "🚗", "icon_name": "directions_car", "order": 11, "desc": "Dealerships, garages, and logistics with instant quote and vehicle inventory engines."},
            {"id": "12", "name": "Beauty & Wellness", "slug": "beauty-wellness", "icon": "💅", "icon_name": "spa", "order": 12, "desc": "Salons, spas, and aesthetic clinics with 24/7 calendar booking and client retention drips."},
            {"id": "13", "name": "Property & Real Estate", "slug": "property", "icon": "🏠", "icon_name": "real_estate_agent", "order": 13, "desc": "Real estate agencies and property developers with buyer qualification chatbots."},
            {"id": "14", "name": "Travel & Tourism", "slug": "travel-tourism", "icon": "✈️", "icon_name": "flight", "order": 14, "desc": "Tour operators and safari companies with custom itinerary builders and payment flows."},
            {"id": "15", "name": "Home & Field Services", "slug": "home-commercial-services", "icon": "🏢", "icon_name": "home_repair_service", "order": 15, "desc": "Contractors, plumbers, and maintenance services with instant quote estimators."},
            {"id": "16", "name": "AI Systems & Automation", "slug": "ai-integration", "icon": "🤖", "icon_name": "smart_toy", "order": 16, "desc": "End-to-end AI workflow automations, CRM syncs, and intelligent operational systems."},
            {"id": "17", "name": "AI Chatbots & Voice Agents", "slug": "ai-chatbot-development", "icon": "💬", "icon_name": "forum", "order": 17, "desc": "24/7 WhatsApp, Web, and Voice AI customer support and lead qualification bots."},
            {"id": "18", "name": "Custom Web Applications", "slug": "custom-web-applications", "icon": "⚙️", "icon_name": "terminal", "order": 18, "desc": "Bespoke SaaS platforms, client portals, and cloud business software."},
            {"id": "19", "name": "AI Lead Generation & Qualification", "slug": "ai-lead-generation", "icon": "🎯", "icon_name": "track_changes", "order": 19, "desc": "Autonomous customer acquisition pipelines, high-intent traffic filters, and cold outreach."},
            {"id": "20", "name": "Pipeline Growth & Re-Engagement", "slug": "customer-growth-re-engagement", "icon": "📈", "icon_name": "trending_up", "order": 20, "desc": "Automated reactivation drips, abandoned cart recovery, and review generation bots."}
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat, _ = ServiceCategory.objects.update_or_create(
                slug=cdata["slug"],
                defaults={
                    "name": cdata["name"],
                    "icon": cdata["icon"],
                    "icon_name": cdata["icon_name"],
                    "description": cdata["desc"],
                    "order": cdata["order"],
                    "is_active": True
                }
            )
            cat_objs[cdata["slug"]] = cat

        # Read SERVICES_LIST.md if present
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        services_md_path = os.path.join(base_dir, "SERVICES_LIST.md")

        seeded_services = []

        # ── 1. Prepend the 58 New High-Value Services ──
        for sdata in NEW_SERVICES:
            cat = cat_objs.get(sdata["category_slug"])
            if not cat:
                continue
            seeded_services.append({
                "category": cat,
                "title": sdata["title"],
                "slug": slugify(sdata["title"]),
                "icon_name": sdata["icon_name"],
                "short_description": sdata["short_description"],
                "overview": sdata["overview"],
                "benefits": sdata["benefits"],
                "process": sdata["process"],
                "image_url": sdata.get("image_url", ""),
            })

        if os.path.exists(services_md_path):
            with open(services_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse categories in markdown
            cat_sections = re.split(r'##\s+[^\n]*Category\s+(\d+)\s+—\s+([^\n]+)', content)
            # cat_sections[0] is preamble, then triplets: (num, title, body)
            for i in range(1, len(cat_sections), 3):
                cat_num = cat_sections[i].strip()
                cat_title = cat_sections[i+1].strip()
                cat_body = cat_sections[i+2]

                # Match slug from body
                slug_match = re.search(r'\*\*Slug:\*\*\s+`([^`]+)`', cat_body)
                cat_slug = slug_match.group(1) if slug_match else slugify(cat_title)

                target_cat = cat_objs.get(cat_slug) or cat_objs.get(list(cat_objs.keys())[int(cat_num)-1 if int(cat_num) <= len(cat_objs) else 0])

                # Split services by '### X. Title'
                service_blocks = re.split(r'###\s+\d+\.\s+([^\n]+)', cat_body)
                for j in range(1, len(service_blocks), 2):
                    title = service_blocks[j].strip()
                    s_body = service_blocks[j+1]

                    desc_m = re.search(r'-\s+\*\*Short Description:\*\*\s+([^\n]+)', s_body)
                    short_desc = desc_m.group(1).strip() if desc_m else f"Elite {title} system with AI Lead Gen and automated client qualification."

                    over_m = re.search(r'-\s+\*\*Overview:\*\*\s+([\s\S]+?)(?=-\s+\*\*Benefits:\*\*|$)', s_body)
                    overview = over_m.group(1).strip() if over_m else ""

                    ben_m = re.search(r'-\s+\*\*Benefits:\*\*\s*([\s\S]+?)(?=-\s+\*\*Process:\*\*|$)', s_body)
                    benefits = ben_m.group(1).strip() if ben_m else ""

                    proc_m = re.search(r'-\s+\*\*Process:\*\*\s*([\s\S]+?)(?=---|\Z)', s_body)
                    process = proc_m.group(1).strip() if proc_m else ""

                    # Clean bullets
                    def clean_bullets(txt):
                        lines = [re.sub(r'^\s*[-*]\s*', '', line).strip() for line in txt.split('\n') if line.strip()]
                        return "\n".join(lines)

                    ben_cleaned = clean_bullets(benefits)
                    proc_cleaned = clean_bullets(process)

                    # Wrap website into the AI Client Acquisition System
                    ai_pitch_desc = f"Revenue-driven {title} digital engine with integrated AI Lead Generation, 24/7 WhatsApp Qualification, and automated customer nurture sequences."
                    ai_pitch_overview = (
                        f"{overview}\n\n"
                        f"⚡ More Than Just A Website — A 24/7 Client Acquisition Engine:\n"
                        f"At UniqueTechCamp, we don't treat your website as a static brochure. We deploy a complete digital revenue system combining a high-performance web storefront with our proprietary AI Lead Generation & Qualification engine. "
                        f"Every visitor is greeted by an intelligent assistant that answers questions, filters serious buyers, captures contact details, and routes qualified leads directly to your WhatsApp or CRM. "
                        f"Integrated automated multi-channel follow-ups (Email & WhatsApp) ensure you never lose a warm lead, turning website visitors into predictable monthly revenue."
                    )

                    ai_benefits = (
                        f"🤖 AI Lead Generation System: High-intent inquiry capture, dynamic cost estimators & interactive lead magnets\n"
                        f"⚡ 24/7 AI Qualification Bot: Pre-screens leads on WhatsApp & Web, filtering high-value clients automatically\n"
                        f"🔄 Automated Multi-Channel Follow-Up: Instant SMS, WhatsApp & Email drip sequences preventing lost deals\n"
                        f"📊 Real-Time Deal Alerts: Immediate notifications sent to your team when a qualified customer is ready to buy\n"
                        f"🚀 High-Speed Conversion Architecture: Ultra-fast loading, mobile-first UX designed to maximize sales\n"
                        f"{ben_cleaned}"
                    )

                    ai_process = (
                        f"1. Revenue Strategy & Customer Journey Mapping: Identifying your high-value buyers and conversion bottlenecks\n"
                        f"2. Conversion-Focused Design & Copywriting: Crafting persuasive layouts, offers, and visual proof\n"
                        f"3. Full-Stack Web Development: Building ultra-fast, secure, and mobile-optimized web pages\n"
                        f"4. AI Lead Gen & Qualification Integration: Deploying 24/7 WhatsApp and website conversational bots\n"
                        f"5. Automated Follow-Up & CRM Setup: Automating instant notifications, reminder drips, and email follow-up\n"
                        f"6. Quality Assurance & Staff Training: End-to-end testing and training your team to handle closed deals\n"
                        f"7. Launch & Ongoing Conversion Tracking: Continuous monitoring and performance optimization"
                    )

                    s_slug = slugify(title)
                    seeded_services.append({
                        "category": target_cat,
                        "title": title,
                        "slug": s_slug,
                        "icon_name": "language",
                        "short_description": ai_pitch_desc,
                        "overview": ai_pitch_overview,
                        "benefits": ai_benefits,
                        "process": ai_process,
                    })

        self.stdout.write(f"Parsed {len(seeded_services)} base services from SERVICES_LIST.md")

        # Additional 40+ high-value industry and AI growth services to guarantee > 100 services (aiming for 114+)
        additional_services = [
            # Healthcare additions
            {
                "cat_slug": "healthcare",
                "title": "Dental Clinics",
                "icon": "dentistry",
                "short_desc": "High-conversion dental practice system with AI smile assessment booking, WhatsApp scheduling, and patient recall automation.",
                "overview": "Complete digital patient acquisition engine for dental clinics. Combines a stunning treatment gallery (implants, orthodontics, cosmetic whitening) with 24/7 AI appointment booking and automated WhatsApp reminder drips that eliminate no-shows.",
            },
            {
                "cat_slug": "healthcare",
                "title": "Cosmetic & Plastic Surgery Clinics",
                "icon": "face",
                "short_desc": "Luxury aesthetic clinic website with confidential AI consultation pre-qualification and procedure financing calculators.",
                "overview": "High-end aesthetic surgery platform engineered to attract and qualify private patients. Features discreet before/after showcases, procedure cost calculators, and an intelligent intake bot that qualifies patient budgets before scheduling specialist consultations.",
            },
            {
                "cat_slug": "healthcare",
                "title": "Physiotherapy & Chiropractic Centers",
                "icon": "accessibility",
                "short_desc": "Patient recovery portal with automated rehabilitation booking, pain assessment quiz, and SMS appointment reminders.",
                "overview": "Engineered for physical therapy and wellness clinics to streamline bookings, qualify injury types, and deliver automated post-session exercise guides directly to patients via WhatsApp.",
            },
            # Retail & Commerce additions
            {
                "cat_slug": "retail-commerce",
                "title": "Jewelry & Luxury Goods Stores",
                "icon": "diamond",
                "short_desc": "Luxury jewelry showcase with bespoke 3D ring visualizers, VIP private viewings, and instant WhatsApp concierge.",
                "overview": "High-ticket luxury e-commerce engine designed for high average order values. Features high-resolution gemstone galleries, custom piece inquiry forms, and a 24/7 AI concierge providing bespoke customer service.",
            },
            {
                "cat_slug": "retail-commerce",
                "title": "Solar & Renewable Energy Equipment Retailers",
                "icon": "solar_power",
                "short_desc": "Clean energy retail system with automated solar power consumption calculator and commercial quotation funnel.",
                "overview": "Engineered to sell solar panels, inverters, and lithium battery backup systems. Features an interactive wattage calculator that qualifies customer power requirements and dispatches immediate site survey quotes to sales reps.",
            },
            # Hospitality additions
            {
                "cat_slug": "hospitality-food",
                "title": "Event Venues & Wedding Gardens",
                "icon": "celebration",
                "short_desc": "High-converting wedding and corporate venue portal with virtual 360 walk-throughs and automated date reservation bots.",
                "overview": "Transforms venue inquiries into high-deposit bookings. Features virtual tours, package pricing estimators, date availability calendars, and instant WhatsApp follow-up for event planners.",
            },
            {
                "cat_slug": "hospitality-food",
                "title": "Luxury Safari Lodges & Camps",
                "icon": "nature_people",
                "short_desc": "Premium lodge booking portal with real-time room availability, safari package visualizer, and international multi-currency checkout.",
                "overview": "Attracts high-value international travelers with immersive wilderness media, seamless safari package booking, and an AI travel assistant providing instantaneous answers to visa, packing, and seasonal migration questions.",
            },
            # Professional Services additions
            {
                "cat_slug": "professional-services",
                "title": "Corporate Accounting & Tax Advisory Firms",
                "icon": "account_balance",
                "short_desc": "B2B accounting platform with tax compliance audit funnels, secure client document portal, and automated retainer onboarding.",
                "overview": "Positions your CPA and tax advisory firm as the go-to corporate authority. Generates inbound SME retainer clients through free tax health check quizzes and automated proposal generation.",
            },
            {
                "cat_slug": "professional-services",
                "title": "Executive Recruitment & HR Agencies",
                "icon": "group",
                "short_desc": "Talent acquisition portal with candidate resume parsing, employer staffing requests, and automated skill-screening bots.",
                "overview": "Dual-sided recruitment engine that attracts high-paying corporate hiring managers while simultaneously screening and qualifying candidates through automated questionnaires.",
            },
            # Automotive additions
            {
                "cat_slug": "automotive",
                "title": "Car Rental & Chauffeur Services",
                "icon": "car_rental",
                "short_desc": "Fleet booking engine with instant vehicle availability, automated driver dispatching, and mobile payment gateways.",
                "overview": "Modern car hire platform for tourists and corporate fleets. Customers pick dates, select vehicles, upload licenses, and pay deposits with real-time automated booking confirmation via WhatsApp and SMS.",
            },
            {
                "cat_slug": "automotive",
                "title": "Auto Body & Custom Modification Shops",
                "icon": "build",
                "short_desc": "Visual portfolio for custom vehicle builds, paint protection, and instant body repair photo estimate bots.",
                "overview": "Allows vehicle owners to snap and upload dent/scratch photos for instant AI-assisted repair estimates, booking service appointments directly into shop schedules.",
            },
            # Beauty & Wellness additions
            {
                "cat_slug": "beauty-wellness",
                "title": "Gyms, Crossfit & Fitness Studios",
                "icon": "fitness_center",
                "short_desc": "Fitness club membership portal with class schedules, trainer booking, and automated trial pass follow-up funnels.",
                "overview": "Captures fitness enthusiasts with 3-day guest passes, automatically qualifies fitness goals via WhatsApp, and nurtures prospects until they convert into annual recurring gym members.",
            },
            # Property additions
            {
                "cat_slug": "property",
                "title": "Commercial Office & Co-Working Spaces",
                "icon": "domain",
                "short_desc": "Flexible workspace leasing platform with private desk booking, floor plan visualizers, and virtual tour scheduling.",
                "overview": "Drives office occupancy for commercial towers and coworking hubs. Prospective tenants book physical tours with an automated calendar bot that follows up with lease brochures and customized pricing.",
            },
            {
                "cat_slug": "property",
                "title": "Short-Term Vacation Rentals & Airbnb Hosts",
                "icon": "cottage",
                "short_desc": "Direct booking website for luxury Airbnb and vacation rentals avoiding 15% platform commissions with automated guest guides.",
                "overview": "Enables vacation property owners to take commission-free direct bookings with secure M-Pesa / card payments and automated guest check-in instructions delivered via WhatsApp.",
            },
            # Home & Field Services additions
            {
                "cat_slug": "home-commercial-services",
                "title": "Commercial Cleaning & Fumigation Services",
                "icon": "cleaning_services",
                "short_desc": "Commercial cleaning portal with square-footage price estimator, recurring contract setup, and automated supervisor dispatch.",
                "overview": "Generates steady commercial cleaning contracts from corporate offices and residential estates using automated quote calculators and instant proposal emails.",
            },
            {
                "cat_slug": "home-commercial-services",
                "title": "Private Security & CCTV Installation Companies",
                "icon": "security",
                "short_desc": "Premises security system with risk assessment quiz, guard patrol quotation tool, and alarm monitoring inquiry funnels.",
                "overview": "Positions your security firm to win corporate and residential estate protection tenders through structured vulnerability audit funnels and automated executive follow-up.",
            },
            # AI Lead Generation & Qualification Category (Category 15)
            {
                "cat_slug": "ai-lead-generation",
                "title": "Autonomous Inbound Lead Qualification Engines",
                "icon": "psychology",
                "short_desc": "Smart conversational bots embedded on your website and WhatsApp that pre-screen every inbound lead 24/7.",
                "overview": "Never waste sales time on unqualified tire-kickers again. Our Autonomous Inbound Lead Qualification Engine greets visitors instantly, asks strategic screening questions (budget, timeline, authority, exact pain points), scores the lead, and books qualified buyers directly into your calendar.",
            },
            {
                "cat_slug": "ai-lead-generation",
                "title": "Multi-Channel WhatsApp Sales Automation Bots",
                "icon": "chat",
                "short_desc": "Turn WhatsApp into an automated closing machine with instant product catalogues, intelligent FAQ handling, and payment links.",
                "overview": "In Africa and global markets, deals close on WhatsApp. We build enterprise WhatsApp Business API bots that showcase your products, answer complex questions, calculate quotes, and accept payments 24 hours a day without human delay.",
            },
            {
                "cat_slug": "ai-lead-generation",
                "title": "AI B2B Cold Outreach & Pipeline Infrastructure",
                "icon": "send",
                "short_desc": "Automated prospecting system that identifies decision-makers, crafts personalized messages, and books meetings on autopilot.",
                "overview": "Fill your sales calendar with qualified corporate decision-makers. We engineer domain reputation protection, verified lead scraping, dynamic hyper-personalized email & LinkedIn sequences, and AI reply classification that alerts you the second a prospect shows buying interest.",
            },
            {
                "cat_slug": "ai-lead-generation",
                "title": "Instant AI Voice Inbound Receptionist",
                "icon": "phone_in_talk",
                "short_desc": "Human-sounding AI telephone agent that answers phone calls, answers customer questions, and books appointments 24/7.",
                "overview": "Never miss another inbound customer phone call while on a job or after business hours. Our ultra-low latency AI voice agents speak fluently, handle customer inquiries, capture lead details, and synchronize bookings straight into your calendar.",
            },
            {
                "cat_slug": "ai-lead-generation",
                "title": "Predictive Lead Scoring & CRM Enrichment",
                "icon": "insights",
                "short_desc": "AI algorithm that analyzes lead behavior, enriches social profiles, and flags your highest-value prospects in real time.",
                "overview": "Stop guessing which leads will buy. Our predictive scoring engine tracks user interactions across your website, enriches company revenue and employee data from public registries, and scores leads so your sales team contacts the most profitable deals first.",
            },
            {
                "cat_slug": "ai-lead-generation",
                "title": "High-Intent Dynamic Landing Page Personalization",
                "icon": "auto_awesome",
                "short_desc": "AI landing pages that dynamically adapt headlines, testimonials, and offers based on the visitor's industry and traffic source.",
                "overview": "Skyrocket your conversion rates by showing each prospect exactly what they came for. If a dentist visits from Google Ads, the page adapts to showcase dental case studies and dental pricing; if a hotelier visits, it adapts instantly to hospitality.",
            },
            {
                "cat_slug": "ai-lead-generation",
                "title": "Automated Multi-Touch Cold Prospecting Sequences",
                "icon": "alt_route",
                "short_desc": "Multi-channel outreach across Email, SMS, and WhatsApp with intelligent response tracking and calendar synchronization.",
                "overview": "Consistently fill your sales pipeline with verified target accounts through multi-stage automated outreach sequences that stop automatically when a lead responds or books a consultation.",
            },
            # Customer Pipeline Growth & Re-Engagement Category (Category 16)
            {
                "cat_slug": "customer-growth-re-engagement",
                "title": "Dormant Customer Reactivation AI Drips",
                "icon": "history",
                "short_desc": "Automated AI campaigns that re-engage past buyers and lost opportunities, unlocking hidden revenue without ad spend.",
                "overview": "Your past database is an unmined goldmine. Our Dormant Reactivation Engine sends tailored, contextual check-ins and special VIP upgrade offers to past clients, turning silent contacts back into active paying repeat customers.",
            },
            {
                "cat_slug": "customer-growth-re-engagement",
                "title": "Abandoned Cart & Checkout WhatsApp Recovery Bots",
                "icon": "remove_shopping_cart",
                "short_desc": "Instant WhatsApp recovery messages that recover 20-35% of lost online sales with personalized discount offers.",
                "overview": "Standard email abandoned cart sequences only get a 10% open rate. Our WhatsApp checkout recovery bots trigger within 15 minutes with a 98% open rate, offering instant customer support, answering payment doubts, and securing the order.",
            },
            {
                "cat_slug": "customer-growth-re-engagement",
                "title": "Automated Review & Reputation Generation Engines",
                "icon": "star",
                "short_desc": "System that automatically triggers 5-star Google Review requests upon successful client delivery while filtering negative feedback.",
                "overview": "Dominate local Google Search rankings. Our system detects completed orders or service appointments, automatically reaches out to satisfied clients for a Google Review, and routes any complaints privately to management.",
            },
            {
                "cat_slug": "customer-growth-re-engagement",
                "title": "VIP Referral & Affiliate Partner Automation",
                "icon": "handshake",
                "short_desc": "Turn existing happy clients into your best sales reps with automated referral tracking and commission payouts.",
                "overview": "Automate word-of-mouth growth. Gives each client a unique referral portal and rewards them automatically via M-Pesa or bank transfer whenever someone they introduce signs a contract.",
            },
            {
                "cat_slug": "customer-growth-re-engagement",
                "title": "Automated Upsell & Subscription Renewal Engines",
                "icon": "autorenew",
                "short_desc": "Intelligent retention workflows that trigger timely upsell offers, maintenance reminders, and renewal invoices.",
                "overview": "Maximize Customer Lifetime Value (LTV). Our engine tracks service expiry dates and customer consumption cycles, automatically sending maintenance reminders and upgrade proposals before contracts expire.",
            },
            {
                "cat_slug": "customer-growth-re-engagement",
                "title": "Real-Time Executive Growth & Conversion Dashboards",
                "icon": "dashboard",
                "short_desc": "Live executive analytics dashboard tracking lead acquisition costs, conversion rates, and revenue pipeline in real-time.",
                "overview": "Get clear visibility into your entire business growth machine. See live cost-per-lead, pipeline deal velocity, top-performing channels, and bot conversion metrics in one clean executive command center.",
            },
            # Education additions
            {
                "cat_slug": "education",
                "title": "Coding & Tech Bootcamps",
                "icon": "code",
                "short_desc": "Modern tech academy platform with interactive curriculum syllabus, portfolio showcase, and student admission funnels.",
                "overview": "Engineered specifically for technology training academies and coding institutes. Features course preview modules, student project galleries, tuition financing options, and an automated WhatsApp admissions advisor.",
            },
            # Religious addition
            {
                "cat_slug": "religious-organizations",
                "title": "Non-Profit Foundations & Community NGOs",
                "icon": "volunteer_activism",
                "short_desc": "Global donor fundraising portal with multi-currency contributions, impact storytelling, and annual report archives.",
                "overview": "Builds international credibility for NGOs and charities. Includes transparent project trackers, automated donor tax receipts, and recurrent sponsorship pledge funnels.",
            },
            # Travel addition
            {
                "cat_slug": "travel-tourism",
                "title": "Adventure Sports & Mountaineering Expeditions",
                "icon": "hiking",
                "short_desc": "High-adrenaline excursion portal with gear checklist downloads, fitness requirements quiz, and group expedition bookings.",
                "overview": "Designed for mountain climbing, rafting, and outdoor adventure companies. Qualifies participant fitness levels, manages digital liability waivers, and automates expedition deposit collections.",
            }
        ]

        for sdata in additional_services:
            cat = cat_objs.get(sdata["cat_slug"])
            if not cat:
                continue

            title = sdata["title"]
            s_slug = slugify(title)

            ai_pitch_desc = sdata["short_desc"]
            ai_pitch_overview = (
                f"{sdata['overview']}\n\n"
                f"⚡ End-To-End Customer Acquisition & Growth Engine:\n"
                f"This service is architected as an end-to-end client generation machine. From search discovery to final sale, our integrated AI Lead Qualification Bot engages incoming traffic immediately, qualifies buyer budget and urgency, and triggers multi-channel follow-up sequences to secure the transaction without manual delays."
            )

            ai_benefits = (
                f"🤖 AI Lead Generation System: Captures high-intent prospects via interactive qualification funnels\n"
                f"⚡ 24/7 AI WhatsApp & Web Qualification: Pre-screens leads, filters low-budget queries, and books appointments\n"
                f"🔄 Automated Multi-Touch Follow-Up: Instant SMS, WhatsApp & Email drip campaigns preventing deal slippage\n"
                f"📱 Instant Sales Alerts: Immediate push notifications to your team when a hot deal is ready to close\n"
                f"📊 Built-in CRM Pipeline Integration: Automatically tracks every deal from cold visitor to paid client\n"
                f"🛡️ High-Performance Architecture: 99.9% uptime, bank-grade encryption, and sub-second load times\n"
                f"🌐 Local & Global SEO Dominance: Structured data for top Google Search and Maps placement"
            )

            ai_process = (
                f"1. Growth Strategy & Funnel Architecture: Mapping target buyer personas, key value propositions, and sales milestones\n"
                f"2. Bespoke UI/UX Design: Crafting high-converting, mobile-first layouts and interactive visual components\n"
                f"3. Production Engineering: Fast, clean, accessible code built on modern web standards\n"
                f"4. AI Lead Gen & Qualification Setup: Training conversational bots on your business services, pricing, and FAQs\n"
                f"5. Follow-Up Workflow Automation: Connecting CRM, email drips, and instant WhatsApp alerts\n"
                f"6. End-to-End System Validation: Rigorous cross-device testing and conversion rate optimization\n"
                f"7. Launch & Ongoing Revenue Analytics: Continuous tracking of visitors, leads, and closed sales"
            )

            seeded_services.append({
                "category": cat,
                "title": title,
                "slug": s_slug,
                "icon_name": sdata["icon"],
                "short_description": ai_pitch_desc,
                "overview": ai_pitch_overview,
                "benefits": ai_benefits,
                "process": ai_process,
            })

        self.stdout.write(f"Total service models prepared for database: {len(seeded_services)}")

        # Insert or update into database
        count = 0
        for idx, item in enumerate(seeded_services):
            # Ensure unique slug
            unique_slug = item["slug"]
            if Service.objects.filter(slug=unique_slug).exclude(title=item["title"]).exists():
                unique_slug = f"{unique_slug}-{item['category'].id}"

            is_feat = (idx % 7 == 0)
            defaults = {
                "category": item["category"],
                "title": item["title"],
                "icon_name": item["icon_name"],
                "short_description": item["short_description"][:255],
                "overview": item["overview"],
                "benefits": item["benefits"],
                "process": item["process"],
                "order": idx + 1,
                "is_active": True,
                "is_featured": is_feat,
            }
            if item.get("image_url"):
                defaults["image_url"] = item["image_url"]

            Service.objects.update_or_create(
                slug=unique_slug,
                defaults=defaults
            )
            count += 1

        total_cats = ServiceCategory.objects.count()
        total_servs = Service.objects.count()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded database! Total Categories: {total_cats} | Total Services: {total_servs}"
        ))
