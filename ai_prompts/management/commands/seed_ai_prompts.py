import decimal
from django.core.management.base import BaseCommand
from ai_prompts.models import PromptCategory, AIPrompt


class Command(BaseCommand):
    help = "Seeds initial high-converting AI Master Coding Prompts into the catalog"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding AI Prompt Categories and Master Prompts...")

        # 1. Categories
        cat_sheets, _ = PromptCategory.objects.get_or_create(
            name="Google Apps Script & Sheets",
            defaults={
                'slug': 'google-apps-script-sheets',
                'icon': 'table',
                'description': 'Production Google Sheets dashboards, web apps, and Apps Script automations.',
                'order': 1,
            }
        )

        cat_ai_whatsapp, _ = PromptCategory.objects.get_or_create(
            name="AI Chatbots & WhatsApp Automation",
            defaults={
                'slug': 'ai-chatbots-whatsapp-automation',
                'icon': 'bot',
                'description': '24/7 qualification chatbots, WhatsApp Business Cloud API workflows, and lead bots.',
                'order': 2,
            }
        )

        cat_web, _ = PromptCategory.objects.get_or_create(
            name="Full-Stack Web Applications",
            defaults={
                'slug': 'full-stack-web-applications',
                'icon': 'layout',
                'description': 'Modern web portals, customer dashboards, and high-performance business engines.',
                'order': 3,
            }
        )

        cat_ecommerce, _ = PromptCategory.objects.get_or_create(
            name="E-Commerce & Retail POS",
            defaults={
                'slug': 'ecommerce-retail-pos',
                'icon': 'shopping-bag',
                'description': 'Point-of-sale systems, multi-vendor stores, and automated billing with M-Pesa.',
                'order': 4,
            }
        )

        cat_crm_erp, _ = PromptCategory.objects.get_or_create(
            name="CRM & ERP Systems",
            defaults={
                'slug': 'crm-erp-systems',
                'icon': 'briefcase',
                'description': 'Enterprise resource planning, property deals, clinic desks, and school portals.',
                'order': 5,
            }
        )

        # 2. Prompts
        # Prompt 1: Car Marketplace (Rameez Scripts Inspired)
        p1, created = AIPrompt.objects.get_or_create(
            slug="car-marketplace-admin-dealer-dashboard-apps-script",
            defaults={
                'category': cat_sheets,
                'title': "Build a Complete Car Marketplace with Google Sheets & Apps Script | Admin & Dealer Dashboard",
                'tagline': "Complete multi-dealer vehicle marketplace web app backed 100% by Google Sheets and Apps Script.",
                'overview': """Turn Google Sheets into a high-octane Car Marketplace and Dealership Management web application.

This production-grade system provides:
1. **Public Vehicle Marketplace Portal**: Clean, modern car search with multi-parameter filtering (Make, Model, Year, Fuel Type, Transmission, Budget Range in KES/USD).
2. **Dealer Account Portal**: Independent car dealers can log in, manage inventory, upload photos directly to Google Drive folders, print PDF invoices, and receive WhatsApp lead inquiries.
3. **Super Admin Dashboard**: Full control over listed dealerships, commission tracking, vehicle approvals, and performance metrics.
4. **Google Sheets Database**: Zero monthly server bills. The database resides in your Google Drive with sheets for `Cars`, `Dealers`, `Inquiries`, `Transactions`, and `AuditLogs`.

Modeled after modern SaaS design standards with responsive Tailwind CSS, high-converting WhatsApp action buttons, and automated email alerts.""",
                'master_prompt': """You are an elite Principal Full-Stack Engineer and Google Workspace Automation Architect.
Your task is to build a complete, production-ready Car Marketplace and Dealership Management Web App built entirely on Google Apps Script (HTMLService) with Google Sheets as the backend database.

### 1. SYSTEM ARCHITECTURE & GOOGLE SHEETS SCHEMA
Create a Google Spreadsheet with 5 tabs:
1. `Cars`: [car_id, dealer_id, title, make, model, year, mileage, price_kes, price_usd, fuel_type, transmission, condition, drive_image_ids, status (active/sold/pending), created_at]
2. `Dealers`: [dealer_id, business_name, owner_name, email, phone_number, password_hash, logo_drive_id, verification_status, created_at]
3. `Inquiries`: [inquiry_id, car_id, customer_name, customer_phone, customer_email, message, status (new/contacted/closed), timestamp]
4. `Transactions`: [tx_id, dealer_id, car_id, sale_price, payment_ref, commission_kes, date]
5. `Config`: [key, value] (Till number, support WhatsApp, admin email)

### 2. BACKEND APPS SCRIPT CODE (Code.gs)
- `doGet(e)`: Route dispatcher handling:
  - Default route: Public marketplace catalog with live search & filters.
  - `?page=car&id=...`: Vehicle detail view with photo gallery & WhatsApp buy button.
  - `?page=dealer`: Dealer login and dashboard.
  - `?page=admin`: Super Admin console.
- Secure session tokens using CacheService or UserProperties.
- `apiGetCars(filters)`: High performance JSON query engine filtering by make, budget, transmission.
- `apiUploadVehicleImage(base64Data, filename)`: Saves files directly into dedicated Google Drive folder and returns Drive Image ID.
- `apiSubmitInquiry(inquiryData)`: Appends inquiry to sheet and dispatches automated WhatsApp alert to dealer (+254...) and confirmation email to buyer.

### 3. FRONTEND UI SPECIFICATIONS (Index.html, Dealer.html, Admin.html)
- Responsive Tailwind CSS (loaded via CDN) with modern slate-950 dark theme and emerald green accent (#22C55E).
- Lucide icons for car specs (speedometer, gas pump, calendar, tag).
- Live currency toggle between KES (Kenya Shillings) and USD.
- Click-to-WhatsApp button with pre-filled message: "Hello! I am inquiring about [Car Title] listed on your marketplace for KES [Price]."
- Google Drive image carousel with lightbox modal.
- Dealer Inventory CRUD modal with photo upload drag-and-drop.
- Toast notifications for all actions.

### 4. PRODUCTION READINESS
- Strict input sanitization to prevent XSS.
- Error handling with user-friendly alerts.
- Instructions on how to deploy as Web App (Execute as: Me, Who has access: Anyone).""",
                'system_instructions': """1. Open Google Sheets and create a new blank spreadsheet titled 'Car Marketplace Database'.
2. Click Extensions > Apps Script to launch the script editor.
3. Paste the provided Code.gs master script into Code.gs.
4. Create the corresponding HTML files (Index.html, Dealer.html, Admin.html, Styles.html).
5. Click Deploy > New Deployment > Web App.
6. Set 'Execute as: Me' and 'Who has access: Anyone'.
7. Copy your Web App URL and test live in browser!
8. Need custom adaptation or domain setup? Contact UniqueTechCamp with Till 5797853.""",
                'features_list': """Multi-Dealer Accounts with Individual Inventory Management
Google Drive Image Upload & Automated Thumbnail Resizing
Dual Currency Display (KES & USD) with Dynamic Switcher
One-Click WhatsApp Customer Lead Redirection
Google Sheets Real-Time Database (Zero Hosting Cost)
Super-Admin Approval & Commission Tracking Console
PDF Invoice Generator for Closed Car Deals
Full Source Code Ready for Claude Code & Cursor""",
                'prerequisites': "Google Account (Gmail or Google Workspace), Google Drive, Web Browser.",
                'tech_stack': "Google Apps Script, Google Sheets API, HTML5, Tailwind CSS, Lucide Icons, WhatsApp API",
                'target_ai_tools': "Claude Code, Cursor, Windsurf, ChatGPT-4o",
                'difficulty_level': "Intermediate",
                'is_free': False,
                'price_kes': decimal.Decimal("1500.00"),
                'price_usd': decimal.Decimal("12.00"),
                'assistance_price_kes': decimal.Decimal("2500.00"),
                'assistance_price_usd': decimal.Decimal("20.00"),
                'youtube_url': "https://www.youtube.com/watch?v=hmun3dE--vA",
                'copy_count': 142,
                'view_count': 980,
                'download_count': 78,
                'is_featured': True,
                'is_published': True,
            }
        )

        # Prompt 2: Clinic & Hospital Appointment Booking with WhatsApp AI Bot
        p2, created = AIPrompt.objects.get_or_create(
            slug="clinic-hospital-appointment-system-whatsapp-ai-bot",
            defaults={
                'category': cat_ai_whatsapp,
                'title': "24/7 Clinic & Hospital Appointment Booking System with Automated WhatsApp AI Bot",
                'tagline': "Self-service patient appointment booking engine with automatic 24/7 WhatsApp triage and reminders.",
                'overview': """Deploy an enterprise-grade Patient Booking, Doctor Scheduling, and automated 24/7 WhatsApp qualification system for health clinics, dental offices, and hospitals.

Includes:
1. **Patient Booking Portal**: Allows patients to choose department, doctor, date, and time slot.
2. **24/7 WhatsApp AI Bot**: Automatically handles patient FAQs, pre-qualifies symptoms, confirms appointment slots, and sends automated 24-hour and 2-hour appointment reminders.
3. **Doctor & Staff Desk**: Live calendar showing patient queues, consultation statuses, and electronic medical record (EMR) notes.
4. **M-Pesa STK Consultation Fee Integration**: Seamless deposit or consultation fee payment to Till 5797853.""",
                'master_prompt': """You are a Lead Healthcare Systems Architect and Python/Django + AI Engineer.
Develop a complete Clinic Appointment Booking System integrated with WhatsApp Business Cloud API and Django 5.1.

### CORE MODULES
1. `departments` & `doctors`: Doctors with working hours, consultation fee in KES and USD, bio, and specialties.
2. `appointments`: Patient name, phone number (validated with +country code e.g. +254...), email, doctor, time slot, status (Confirmed/Pending/Cancelled), payment_status.
3. `whatsapp_bot`: Webhook receiver for Meta WhatsApp Cloud API:
   - Interactive list messages for selecting department and available doctor.
   - Date picker simulation and slot validation.
   - Automated 24-hour reminder Celery/cron task dispatching patient reminders with Google Maps directions.

### UI DESIGN SPECIFICATIONS
- Tailwind CSS with clean medical green and deep slate palette.
- Modern slot grid highlighting available vs booked slots.
- Dual currency pricing: KES 2,500 / $25 USD consultation fee.
- Mobile bottom navigation dock for instant appointment booking.
- Admin dashboard powered by Django Unfold.""",
                'system_instructions': """1. Clone Django project or create new virtualenv.
2. Run prompt in Claude Code or Cursor: 'claude code -p prompt.md'.
3. Configure WhatsApp Cloud API credentials in .env.
4. Run migrations and start server.""",
                'features_list': """24/7 WhatsApp Autonomous Booking Bot
Multi-Doctor Live Calendar & Real-Time Availability Sync
Automated SMS & WhatsApp Reminder Dispatches
Patient Electronic Medical Records (EMR) Notes
Safaricom M-Pesa Consultation Fee Collection
UK English & Nairobi Kenya Timezone (EAT) Compliance""",
                'prerequisites': "Python 3.11+, WhatsApp Business Account / Meta Developer Account, Redis.",
                'tech_stack': "Python, Django, Tailwind CSS, Celery, Redis, WhatsApp Cloud API",
                'target_ai_tools': "Claude Code, Cursor, Windsurf, ChatGPT-4o",
                'difficulty_level': "Advanced",
                'is_free': False,
                'price_kes': decimal.Decimal("2000.00"),
                'price_usd': decimal.Decimal("15.00"),
                'assistance_price_kes': decimal.Decimal("3500.00"),
                'assistance_price_usd': decimal.Decimal("30.00"),
                'youtube_url': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                'copy_count': 89,
                'view_count': 640,
                'download_count': 45,
                'is_featured': True,
                'is_published': True,
            }
        )

        # Prompt 3: Real Estate CRM & Deal Machine
        p3, created = AIPrompt.objects.get_or_create(
            slug="real-estate-deal-pipeline-crm-lead-machine",
            defaults={
                'category': cat_crm_erp,
                'title': "Real Estate Deal Pipeline & Lead Acquisition Engine with WhatsApp Chatbot",
                'tagline': "Complete property listings portal with Kanban deal pipeline and automatic lead qualification.",
                'overview': """Turn real estate traffic into closed property deals with this complete Property Catalog + CRM Pipeline.

Designed specifically for property developers, agency brokers, and land realtors in Kenya and international markets. Includes interactive map pins, video walkthrough embeds, downloadable brochures, and an automated agent dispatch pipeline.""",
                'master_prompt': """You are a Senior SaaS Engineer. Build a Real Estate Lead Acquisition and Deal Pipeline CRM Web Application.

### KEY FEATURES
1. Property Listings with bedrooms, bathrooms, square footage, KES / USD pricing, and Google Maps pin.
2. Instant WhatsApp Lead Bot: When visitor clicks 'Inquire', bot immediately qualifies budget, move-in timeline, and schedules a site visit.
3. Broker Kanban CRM: Drag-and-drop deal stages: New Lead -> Site Visit Scheduled -> Offer Made -> Legal Due Diligence -> Closed Won.
4. Automated property brochure PDF generation.""",
                'system_instructions': """Paste into Cursor, Windsurf, or Claude Code. Follow the setup steps to configure property schemas and interactive Kanban board.""",
                'features_list': """Interactive Property Catalog with Multi-Filter Search
Kanban Drag-and-Drop Deal Pipeline
WhatsApp Lead Auto-Capture
Brochure PDF Exporter
Dual Currency Support (KES & USD)""",
                'prerequisites': "Modern browser, Node.js or Python environment.",
                'tech_stack': "Django, Tailwind CSS, Lucide Icons, SQLite/MySQL, WhatsApp API",
                'target_ai_tools': "Claude Code, Cursor, Windsurf, Gemini",
                'difficulty_level': "Beginner",
                'is_free': True,
                'price_kes': decimal.Decimal("0.00"),
                'price_usd': decimal.Decimal("0.00"),
                'assistance_price_kes': decimal.Decimal("2500.00"),
                'assistance_price_usd': decimal.Decimal("20.00"),
                'youtube_url': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                'copy_count': 230,
                'view_count': 1420,
                'download_count': 180,
                'is_featured': True,
                'is_published': True,
            }
        )

        # Prompt 4: Retail POS & E-Commerce with M-Pesa STK
        p4, created = AIPrompt.objects.get_or_create(
            slug="full-stack-retail-pos-ecommerce-mpesa-engine",
            defaults={
                'category': cat_ecommerce,
                'title': "Full-Stack E-Commerce & Retail POS Engine with M-Pesa STK Push & Google Sheets Sync",
                'tagline': "High-speed cashier POS barcode scanner + online storefront with instant Safaricom M-Pesa checkout.",
                'overview': """A dual-channel commerce engine: Operate your retail physical store cashier counter with barcode scanner support, and simultaneously sell to online customers with automated M-Pesa STK Push checkout.

Syncs all inventory changes automatically to Google Sheets or SQL database so you never oversell stock.""",
                'master_prompt': """You are a Principal FinTech & E-Commerce Architect.
Build a complete Retail Point of Sale (POS) and Customer Storefront with Safaricom Daraja M-Pesa STK Push integration.

### ARCHITECTURE
1. POS Terminal with barcode scanner input (camera or USB scanner), receipt printer format (thermal 80mm), and daily cash drawer reconciliation.
2. Online storefront with cart, instant checkout, and M-Pesa STK Push dialog.
3. Automated Safaricom Daraja callback processor updating order to 'Paid' instantly.
4. Support for Till: 5797853 and Paybill numbers.""",
                'system_instructions': """Run in Claude Code or Cursor. Setup Safaricom Daraja consumer key and secret in .env.""",
                'features_list': """High-Speed POS Counter with Thermal Receipt Output
Safaricom Daraja 2.0 M-Pesa STK Push Integration
Real-Time Inventory Low-Stock Alerts
Google Sheets Automatic Sales Log Sync
Dual Currency Switcher (KES & USD)""",
                'prerequisites': "Safaricom Developer Account / Till Number, Python 3.10+",
                'tech_stack': "Python, Django, Tailwind CSS, Daraja API, WebRTC Barcode Scanner",
                'target_ai_tools': "Claude Code, Cursor, Windsurf, ChatGPT-4o",
                'difficulty_level': "Master",
                'is_free': False,
                'price_kes': decimal.Decimal("2500.00"),
                'price_usd': decimal.Decimal("20.00"),
                'assistance_price_kes': decimal.Decimal("4000.00"),
                'assistance_price_usd': decimal.Decimal("35.00"),
                'youtube_url': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                'copy_count': 114,
                'view_count': 780,
                'download_count': 62,
                'is_featured': False,
                'is_published': True,
            }
        )

        # Prompt 5: School ERP
        p5, created = AIPrompt.objects.get_or_create(
            slug="school-college-erp-fee-invoicing-exam-attendance",
            defaults={
                'category': cat_crm_erp,
                'title': "School & College Management ERP: Fees, Exam Seating, Attendance & WhatsApp Student Portal",
                'tagline': "Complete educational institution ERP managing student admissions, automated fee invoices, and exam seating.",
                'overview': """Transform school administration with an automated institution management system.
Handles student admissions, class timetables, teacher assignments, automated term fee invoices with M-Pesa references, and automated student report cards.""",
                'master_prompt': """You are an Enterprise ERP Software Architect.
Build a comprehensive School & Academy Management Web Application.
Modules: Students, Teachers, Classes, Fees with M-Pesa tracking, Exam Seating algorithm, Attendance register, and Parent WhatsApp notice board.""",
                'system_instructions': """Execute prompt in Claude Code. Configure school branding and term schedule in settings.""",
                'features_list': """Automated Term Fee Invoicing with M-Pesa Reference Matching
Exam Hall Seating Optimization Algorithm
Daily Student & Staff Attendance Tracking
Parent Report Card PDF Generator
SMS & WhatsApp Emergency Broadcasts""",
                'prerequisites': "Web server or Google Workspace.",
                'tech_stack': "Python, Django or Google Apps Script, Tailwind CSS, ReportLab PDF",
                'target_ai_tools': "Claude Code, Cursor, Windsurf, ChatGPT-4o",
                'difficulty_level': "Advanced",
                'is_free': False,
                'price_kes': decimal.Decimal("3000.00"),
                'price_usd': decimal.Decimal("25.00"),
                'assistance_price_kes': decimal.Decimal("4500.00"),
                'assistance_price_usd': decimal.Decimal("40.00"),
                'youtube_url': "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                'copy_count': 67,
                'view_count': 510,
                'download_count': 38,
                'is_featured': False,
                'is_published': True,
            }
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded categories and 5 production-ready AI Master Coding Prompts!"))
