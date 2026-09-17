"""
Comprehensive Service Definitions for the 4 Core Business Verticals:
1. 🛠️ Digital Business Setup (14 Services)
2. 📱 Social Media & Digital Marketing (14 Services)
3. 🎨 Graphic Design & Branding (18 Services)
4. 📊 Analytics & Business Intelligence (12 Services)
Total: 58 Premium Revenue-Driven Services
"""

NEW_CATEGORIES = [
    {
        "id": "17",
        "name": "Digital Business Setup",
        "slug": "digital-business-setup",
        "icon": "🛠️",
        "icon_name": "business_center",
        "order": 17,
        "desc": "Turnkey digital infrastructure, Google Business profile setup, custom domain emails, WhatsApp Business automation, and secure payment integrations."
    },
    {
        "id": "18",
        "name": "Social Media & Digital Marketing",
        "slug": "social-media-digital-marketing",
        "icon": "📱",
        "icon_name": "campaign",
        "order": 18,
        "desc": "High-conversion social media campaigns, paid advertising, content creation, brand positioning, and multi-channel audience growth."
    },
    {
        "id": "19",
        "name": "Graphic Design & Branding",
        "slug": "graphic-design-branding",
        "icon": "🎨",
        "icon_name": "palette",
        "order": 19,
        "desc": "Distinctive corporate identity, logo design, marketing collateral, professional company profiles, and print-ready creative assets."
    },
    {
        "id": "20",
        "name": "Analytics & Business Intelligence",
        "slug": "analytics-business-intelligence",
        "icon": "📊",
        "icon_name": "analytics",
        "order": 20,
        "desc": "Actionable data visualization, Google Analytics 4, live sales dashboards, Power BI reporting, and automated predictive business intelligence."
    },
]

NEW_SERVICES = [
    # =========================================================================
    # 🛠️ 1. Digital Business Setup (14 Services)
    # =========================================================================
    {
        "category_slug": "digital-business-setup",
        "title": "Google Business Profile Setup",
        "icon_name": "storefront",
        "short_description": "Complete Google Business Profile setup, PIN/video verification, local Maps SEO optimization, and automated customer review generation.",
        "overview": (
            "Dominate local Google Search and Google Maps. We professionally configure and verify your official Google Business Profile "
            "with geo-tagged photography, keyword-optimized service descriptions, business hours, and direct call/messaging buttons. "
            "Our setup includes local citation consistency, category optimization, and automated QR code review funnels to build 5-star social proof fast."
        ),
        "benefits": (
            "Top Placement on Google Maps & Local 3-Pack search results\n"
            "Official Business Verification with Google badge credibility\n"
            "Direct WhatsApp & Phone Call Action Buttons for local shoppers\n"
            "Automated Review Request Funnel to collect 5-star Google reviews\n"
            "Product & Service Catalog Showcase directly in Google search\n"
            "Real-Time Insights on search impressions, clicks, and calls"
        ),
        "process": (
            "1. Local Market & Keyword Research: Identifying high-intent local search terms in your area\n"
            "2. Profile Creation & Verification Guidance: Managing Google verification via postcard, video, or instant method\n"
            "3. Visual Branding & Geo-Tagging: Uploading high-res store, team, and product photos with geo-coordinates\n"
            "4. Service & Product Menu Setup: Adding full pricing, categories, and direct website links\n"
            "5. Review Funnel & QR Deployment: Providing custom branded Google review links and NFC/QR materials\n"
            "6. Launch & Monthly Local SEO Monitoring: Tracking rank progression and customer call inquiries"
        ),
        "image_url": "https://images.unsplash.com/photo-1572021335469-31706a17aaef?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Business Email Setup",
        "icon_name": "mail",
        "short_description": "Enterprise branded email setup (e.g. name@yourdomain.com) with Google Workspace or Microsoft 365, SPF, DKIM, and DMARC security.",
        "overview": (
            "Upgrade from generic @gmail.com or @yahoo.com addresses to authoritative custom corporate email accounts. "
            "We configure Google Workspace, Microsoft 365, or private cPanel mailboxes with zero-spam SPF, DKIM, and DMARC security records, "
            "seamless mobile/desktop Outlook sync, and unified team signatures."
        ),
        "benefits": (
            "Authoritative Corporate Identity building instant trust with clients\n"
            "Bank-Grade Security with full SPF, DKIM & DMARC anti-spoofing records\n"
            "Zero Inbox Spam Deliverability ensuring your quotes never hit spam\n"
            "Mobile & Desktop Synchronization across iOS, Android, Outlook & Gmail\n"
            "Shared Team Inboxes (e.g. info@, billing@, sales@) with smart routing\n"
            "Automated Cloud Backup preventing loss of confidential correspondence"
        ),
        "process": (
            "1. Architecture Review: Selecting between Google Workspace, M365, or cPanel\n"
            "2. DNS Records Configuration: Adding MX, SPF, DKIM, and DMARC authentication\n"
            "3. User Account Provisioning: Creating personal and departmental mailboxes\n"
            "4. Professional Email Signature Design: Designing branded HTML signatures\n"
            "5. Device Setup & Client Onboarding: Syncing mailboxes across phones and laptops\n"
            "6. Deliverability & Inbound Testing: Verifying 10/10 score on Mail-Tester"
        ),
        "image_url": "https://images.unsplash.com/photo-1596526131083-e8c633c948d2?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Domain Registration",
        "icon_name": "domain",
        "short_description": "Strategic corporate domain name registration (.com, .org, .co.ke, .africa) with DNS management and WHOIS privacy protection.",
        "overview": (
            "Secure your business identity before competitors or squatters take it. We handle strategic brand name search, "
            "global and regional TLD registrations (.com, .co.ke, .io, .ai, .africa), WHOIS identity masking, and enterprise DNS management "
            "with ultra-fast global Anycast nameservers."
        ),
        "benefits": (
            "Trademark & Brand Name Protection across vital domain extensions\n"
            "Complete Ownership & Admin Control with zero lock-in contracts\n"
            "WHOIS Privacy Protection shielding personal phone and home addresses\n"
            "Enterprise Anycast Cloudflare DNS for instant global website routing\n"
            "Auto-Renewal Safeguards preventing accidental domain expiry\n"
            "Free Domain Email Forwarding to your existing personal mailbox"
        ),
        "process": (
            "1. Domain Availability & Trademark Audit: Analyzing brand safety and extension suitability\n"
            "2. Official Registrar Purchase: Registering domain under full client legal ownership\n"
            "3. WHOIS Privacy & Security Shield: Hiding personal contact data from spam crawlers\n"
            "4. High-Speed Cloud DNS Linking: Connecting domain to hosting, email, and landing pages\n"
            "5. SSL Certificate Issuance: Activating HTTPS lock icon on your brand domain\n"
            "6. Handover & Management Training: Handing over direct access credentials"
        ),
        "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Hosting Setup",
        "icon_name": "dns",
        "short_description": "Ultra-fast NVMe SSD cloud hosting setup with automated daily backups, free SSL certificates, and 99.9% uptime guarantees.",
        "overview": (
            "Your website deserves high-speed, secure, and reliable infrastructure. We configure enterprise-grade cloud server hosting "
            "equipped with pure NVMe SSD storage, Redis/Memcached object caching, Cloudflare CDN integration, automated hourly/daily backups, "
            "and active web application firewall (WAF) protection against cyber threats."
        ),
        "benefits": (
            "Sub-Second Page Load Speeds accelerating SEO ranks and conversion rates\n"
            "99.9% High-Availability Uptime SLA for round-the-clock sales\n"
            "Free Enterprise SSL Certificates (HTTPS) with automated renewals\n"
            "Automated Off-Site Backups with 1-click disaster recovery restoration\n"
            "Web Application Firewall (WAF) actively blocking DDoS and brute-force attacks\n"
            "Unlimited Bandwidth & Scalable Server Resources as your traffic grows"
        ),
        "process": (
            "1. Server Sizing & Performance Planning: Calculating database, traffic, and storage needs\n"
            "2. Environment Provisioning: Setting up Linux, Nginx/Apache, and PHP/Python runtimes\n"
            "3. Security Hardening: Configuring firewalls, SSH key security, and brute-force shields\n"
            "4. CDN & Caching Acceleration: Activating Cloudflare global edge network and caching\n"
            "5. Backup Automation: Scheduling automated offsite snapshots to secure cloud storage\n"
            "6. 24/7 Monitoring Deployment: Implementing live uptime alerts via WhatsApp and Email"
        ),
        "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "WhatsApp Business Setup",
        "icon_name": "chat",
        "short_description": "Professional WhatsApp Business account setup with automated greeting sequences, away messages, quick replies, and team access.",
        "overview": (
            "Turn WhatsApp into your primary 24/7 sales machine. We configure your official WhatsApp Business profile with verified contact details, "
            "custom greeting triggers, smart away messages for off-hours, organized chat labels, and high-converting quick reply templates "
            "allowing you to close deals in seconds."
        ),
        "benefits": (
            "Instant Automated Welcome Messages capturing prospects immediately\n"
            "Off-Hours Away Autoresponders keeping leads warm when your team sleeps\n"
            "Pre-Built Quick Reply Shortcuts to answer frequent inquiries in 1 tap\n"
            "Color-Coded Customer Labels organizing leads (New, Quoted, Paid, Shipped)\n"
            "Verified Business Profile Info displaying address, hours, website, and email\n"
            "Direct Click-to-WhatsApp Ads Link ready for Instagram and Facebook marketing"
        ),
        "process": (
            "1. Profile Audit & Phone Number Porting: Transitioning line cleanly to WhatsApp Business\n"
            "2. Company Profile Branding: Uploading logo, bio, operating hours, and location pin\n"
            "3. Autoresponder Scripting: Writing welcoming greeting and away response sequences\n"
            "4. Quick Replies Library: Creating shortcuts for pricing, payment, and account info\n"
            "5. Lead Organization Framework: Setting up CRM tags and color-coded customer labels\n"
            "6. Staff Training: Training your sales reps on response speed and closing etiquette"
        ),
        "image_url": "https://images.unsplash.com/photo-1611746872915-64382b5c76da?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "WhatsApp Catalog Setup",
        "icon_name": "inventory_2",
        "short_description": "Interactive WhatsApp product and service catalog setup with high-resolution imagery, pricing, item descriptions, and direct checkout.",
        "overview": (
            "Let customers browse, select, and purchase your products directly inside WhatsApp without leaving the app. "
            "We organize and publish your complete product or service catalog with high-converting photography, compelling copy, item codes, "
            "and shareable direct links that you can send directly into any chat."
        ),
        "benefits": (
            "In-App Digital Storefront displaying products directly on your WhatsApp profile\n"
            "Instant Shareable Product Links to send exact items into group chats or DMs\n"
            "Cart & Checkout Functionality allowing clients to assemble multiple items\n"
            "Clear Pricing & Deliverables eliminating repetitive back-and-forth inquiries\n"
            "Direct Meta Commerce Sync linking your WhatsApp catalog to Instagram & Facebook\n"
            "High-Resolution Visual Showcase making your offerings look premium"
        ),
        "process": (
            "1. Inventory Audit & Categorization: Structuring products into logical customer collections\n"
            "2. Professional Image Resizing: Optimizing square product photos for mobile screens\n"
            "3. Persuasive Copywriting: Writing concise benefit-driven product descriptions\n"
            "4. Meta Commerce Compliance: Ensuring items comply with WhatsApp commercial policies\n"
            "5. Catalog Publishing: Uploading items, pricing, SKUs, and checkout destination URLs\n"
            "6. Chat Selling Framework: Equipping your team with catalog sharing best practices"
        ),
        "image_url": "https://images.unsplash.com/photo-1556742049-0a67c5574f73?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Social Media Business Pages",
        "icon_name": "share",
        "short_description": "Corporate setup, branding, and optimization of verified business pages on Facebook, Instagram, LinkedIn, and TikTok.",
        "overview": (
            "Establish a consistent, authoritative brand presence across all major social networks. "
            "We create, configure, and brand your corporate Facebook Page, Instagram Professional Account, LinkedIn Company Page, "
            "and TikTok Business account with custom banners, keyword-optimized bios, unified call-to-action buttons, and tracking pixels."
        ),
        "benefits": (
            "Unified Brand Presence across Facebook, Instagram, LinkedIn, and TikTok\n"
            "Custom Branded Banners & Profile Graphics engineered for mobile screens\n"
            "Search-Optimized Bios & Usernames maximizing discoverability in social search\n"
            "Action Buttons Connected (Book Now, WhatsApp, Send Email, Visit Website)\n"
            "Meta Business Suite Integration for unified cross-platform inbox management\n"
            "Pixel & Conversion API Installation ready for high-ROI paid ad campaigns"
        ),
        "process": (
            "1. Platform Strategy: Determining highest-converting networks for your business niche\n"
            "2. Account Registration & Claims: Claiming exact matching handles across all platforms\n"
            "3. Visual Identity Application: Designing matching cover banners, logos, and story highlights\n"
            "4. Bio & Information Engineering: Writing conversion copy with contact links and keywords\n"
            "5. Integration & Verification: Linking WhatsApp Business, Instagram, and Facebook together\n"
            "6. Management Handover: Adding your team as administrators with full security access"
        ),
        "image_url": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Online Booking Setup",
        "icon_name": "calendar_month",
        "short_description": "Automated online appointment scheduling system with live calendar sync, automated client reminders, and cancellation handling.",
        "overview": (
            "Eliminate the endless back-and-forth scheduling calls. We build an automated 24/7 calendar appointment booking system "
            "that integrates with your Google Calendar, Outlook, and website. Features include buffer times between appointments, "
            "custom intake questionnaires, automated WhatsApp/SMS/Email confirmation and reminder sequences, and optional pre-payment deposits."
        ),
        "benefits": (
            "24/7 Self-Service Scheduling allowing clients to book consultations anytime\n"
            "Two-Way Calendar Sync (Google & Outlook) preventing double bookings automatically\n"
            "Automated Email & WhatsApp Reminders cutting no-show rates by up to 80%\n"
            "Intake Questionnaires Gathering key project details before the meeting starts\n"
            "Timezone Auto-Detection for seamless bookings with international clients\n"
            "Integrated Video Meeting Links (Google Meet & Zoom) generated automatically"
        ),
        "process": (
            "1. Availability & Meeting Types Audit: Defining durations, buffer times, and work hours\n"
            "2. Booking Engine Configuration: Setting up custom branded scheduling pages\n"
            "3. Calendar Integration: Connecting live two-way synchronization to your personal calendar\n"
            "4. Reminder Workflow Setup: Writing automated reminder messages (24h and 1h before)\n"
            "5. Website & Social Media Embedding: Adding 'Book Free Consultation' buttons across site\n"
            "6. Live Booking Test: Simulating real client appointment booking and reminders"
        ),
        "image_url": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Payment Integration",
        "icon_name": "credit_card",
        "short_description": "Secure payment gateway integration supporting Visa, Mastercard, PayPal, and Stripe with bank-grade encryption and auto-receipts.",
        "overview": (
            "Collect revenue from customers anywhere in the world. We integrate international and regional credit card payment gateways "
            "(Stripe, PayPal, Pesapal, DPO, Flutterwave) into your website, online store, or invoicing platform. "
            "Includes 3D-Secure 2 authentication, automated PDF receipt generation, and real-time accounting webhooks."
        ),
        "benefits": (
            "Global Credit & Debit Card Processing for Visa, Mastercard & American Express\n"
            "Bank-Grade PCI-DSS Level 1 Compliance with 3D-Secure fraud protection\n"
            "Automated Multi-Currency Support (USD, EUR, GBP, KES) with live conversion\n"
            "Instant Automated PDF Invoice & Receipt Generation dispatched to buyers\n"
            "Recurring Billing & Subscription Capabilities for monthly retainer services\n"
            "Direct Bank Payouts scheduled automatically to your local business account"
        ),
        "process": (
            "1. Merchant Account Onboarding: Assisting with gateway approval and compliance docs\n"
            "2. API & Webhook Integration: Connecting secure checkout SDKs to your website backend\n"
            "3. Security & Fraud Protection: Implementing 3DS2 verification and reCAPTCHA checks\n"
            "4. Receipt & Notification Automation: Designing branded email receipts and payment alerts\n"
            "5. Sandbox Testing: Running test transactions for successful, failed, and refund states\n"
            "6. Live Mode Activation: Switching to production with live card verification"
        ),
        "image_url": "https://images.unsplash.com/photo-1556742111-a301076d9d18?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "M-Pesa Integration",
        "icon_name": "payments",
        "short_description": "Direct Safaricom Daraja M-Pesa API integration for instant STK Push, Paybill, Till Number, and automated payment reconciliation.",
        "overview": (
            "Offer Kenya's most popular payment method directly on your website or digital platform. We integrate Safaricom's Daraja API "
            "to deliver instantaneous M-Pesa STK Push prompts directly to clients' mobile phones, support Paybill and Buy Goods Till numbers, "
            "and automate real-time order status updates without manual confirmation delays."
        ),
        "benefits": (
            "Instant M-Pesa STK Push: Prompts client phone for PIN automatically in seconds\n"
            "Real-Time Instant Reconciliation eliminating manual screenshot checking\n"
            "Support for Paybill, Till Number (Buy Goods), and Business C2B payments\n"
            "Zero Friction Checkout dramatically boosting mobile conversion rates\n"
            "Automated Instant Order Fulfillment and WhatsApp order confirmation alerts\n"
            "Detailed Transaction Dashboard for easy accountant reconciliation"
        ),
        "process": (
            "1. Safaricom Daraja Portal Setup: Creating and verifying developer app credentials\n"
            "2. API Endpoint Implementation: Building secure callback endpoints with validation\n"
            "3. STK Push Checkout UI: Crafting smooth mobile-friendly phone input and loading spinner\n"
            "4. Webhook & Database Sync: Updating order status to 'Paid' upon Safaricom confirmation\n"
            "5. Transaction Alert Notifications: Triggering automated SMS/Email receipts to customer\n"
            "6. Production Go-Live: Requesting live credentials from Safaricom and launching"
        ),
        "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "E-commerce Setup",
        "icon_name": "shopping_bag",
        "short_description": "End-to-end e-commerce store setup with product categories, inventory management, shipping zones, and automated checkout.",
        "overview": (
            "Launch a profitable, high-speed online store engineered to turn visitors into repeat buyers. "
            "We build complete e-commerce architectures featuring product variations (sizes, colors), inventory tracking, "
            "custom shipping rates, tax calculation, coupon engines, abandoned cart recovery, and integrated card/M-Pesa payments."
        ),
        "benefits": (
            "Complete Modern Storefront engineered for ultra-fast mobile navigation\n"
            "Unlimited Product Uploads with variant options, SKU management, and gallery zoom\n"
            "Integrated Multi-Channel Checkout supporting M-Pesa, Cards, and Cash on Delivery\n"
            "Automated Abandoned Cart Email Recovery rescuing lost sales on autopilot\n"
            "Custom Shipping Zones & Rates with pickup location selector options\n"
            "Sales Analytics Dashboard showing daily revenue, top items, and customer stats"
        ),
        "process": (
            "1. Store Architecture & Catalog Planning: Organizing collections, tags, and product filters\n"
            "2. High-Converting Theme Design: Designing mobile-first homepage, product pages, and cart\n"
            "3. Inventory & Pricing Configuration: Setting up taxes, currencies, and shipping zones\n"
            "4. Payment Gateway Deployment: Connecting M-Pesa STK Push, Stripe, and PayPal\n"
            "5. Order Notification Workflow: Setting up instant order alerts via WhatsApp and Email\n"
            "6. End-to-End Test Purchases: Simulating live customer orders and shipping notifications"
        ),
        "image_url": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Online Forms",
        "icon_name": "dynamic_form",
        "short_description": "Smart multi-step digital forms with conditional logic, digital signatures, file upload fields, and instant CRM/email routing.",
        "overview": (
            "Replace messy paper documents and clunky PDFs with smart, mobile-friendly interactive forms. "
            "We build multi-step client intake forms, registration portals, quote calculators, and application questionnaires "
            "featuring conditional logic, document file uploads, digital e-signatures, and instant email/Google Sheets sync."
        ),
        "benefits": (
            "Smart Conditional Logic showing relevant questions based on previous answers\n"
            "Secure File Upload Fields for IDs, resumes, blueprints, and proof of payment\n"
            "Legally Binding Digital E-Signature capture directly on touchscreens\n"
            "Instant Notification Routing sending submissions to Email, WhatsApp, or CRM\n"
            "Automated Google Sheets & Excel Sync updating your database in real-time\n"
            "Spam-Protected Design with invisible reCAPTCHA preventing bot submissions"
        ),
        "process": (
            "1. Form Requirements Analysis: Reviewing your existing paper forms or inquiry steps\n"
            "2. Form Field & Logic Architecture: Structuring intuitive multi-step question progressions\n"
            "3. Responsive UI Styling: Styling inputs with clean validation and mobile keyboards\n"
            "4. Backend Integrations: Connecting webhooks to Google Sheets, CRM, and email alerts\n"
            "5. Confirmation & Autoresponder Setup: Creating custom thank-you pages and email replies\n"
            "6. Testing & Deployment: Verifying validation rules and file upload limits"
        ),
        "image_url": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "QR Code Systems",
        "icon_name": "qr_code_2",
        "short_description": "Custom branded dynamic QR codes for instant website access, vCard contacts, Wi-Fi login, payment links, and analytics tracking.",
        "overview": (
            "Bridge the gap between your physical business and the digital world. We design custom branded dynamic QR codes "
            "embedded with your corporate logo and brand colors. Because our QR codes are dynamic, you can change the destination URL, "
            "menu, or contact card anytime without ever reprinting your physical flyers, signs, or packaging."
        ),
        "benefits": (
            "Dynamic QR Code Technology: Change link destinations anytime without reprinting\n"
            "Custom Branded Visual Design with your company logo and brand color gradients\n"
            "Instant vCard Contact Saving allowing clients to save your number with 1 tap\n"
            "Seamless Touchless Wi-Fi Access for hotels, offices, and coffee shops\n"
            "Real-Time Scan Analytics tracking number of scans, location, and device types\n"
            "High-Resolution Print Files provided in vector SVG, EPS, and high-DPI PNG"
        ),
        "process": (
            "1. Use Case Definition: Determining purpose (website, WhatsApp chat, vCard, menu, payment)\n"
            "2. Dynamic Routing Engine Setup: Creating short tracking URL infrastructure\n"
            "3. Custom Brand Design: Incorporating your logo, rounded eyes, and custom color frames\n"
            "4. Scan Testing Across Devices: Testing readability on iPhone, Samsung, and low-light cameras\n"
            "5. Analytics Dashboard Setup: Connecting scan tracking and conversion event logs\n"
            "6. Print Production Delivery: Delivering vector files ready for printers and signmakers"
        ),
        "image_url": "https://images.unsplash.com/photo-1595079672139-6229431b66b4?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "digital-business-setup",
        "title": "Digital Menu Systems",
        "icon_name": "restaurant_menu",
        "short_description": "Touchless contactless digital menus with QR code scanning, category filtering, high-resolution dish imagery, and WhatsApp ordering.",
        "overview": (
            "Transform your dining experience with ultra-fast digital menus designed for restaurants, bars, and cafes. "
            "Guests simply scan a table QR code with their phone camera to browse interactive food and drink menus with high-res photos, "
            "dietary badges (vegan, gluten-free), live price updates, and instant WhatsApp table ordering."
        ),
        "benefits": (
            "Instant Touchless Dining Experience requiring zero app downloads for diners\n"
            "Live Real-Time Updates: Edit prices, out-of-stock items, and daily specials in seconds\n"
            "Appetizing Visual Layouts with professional photography proven to increase average check size\n"
            "Dietary & Allergen Filtering: Categorize vegan, halal, spicy, and allergy safe items\n"
            "Direct Table WhatsApp Ordering sending selected dishes directly to the kitchen\n"
            "Zero Printing Costs saving thousands in reprinted physical menu costs annually"
        ),
        "process": (
            "1. Menu Digitization & Categorization: Organizing food, beverages, and dessert sections\n"
            "2. Photography Optimization: Retouching and resizing dish photos for mouthwatering display\n"
            "3. Mobile-First Menu Development: Engineering fast-loading, swipeable digital menu web apps\n"
            "4. Table QR Stand Design: Designing branded acrylic table stands with scan instructions\n"
            "5. Staff & Kitchen Workflow Training: Teaching staff how to update items and receive orders\n"
            "6. Launch & Diner Feedback: Reviewing guest scan engagement and popular item analytics"
        ),
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80"
    },

    # =========================================================================
    # 📱 2. Social Media & Digital Marketing (14 Services)
    # =========================================================================
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Social Media Management",
        "icon_name": "hub",
        "short_description": "End-to-end management of corporate social media channels with daily engagement, strategic posting, and multi-platform growth.",
        "overview": (
            "Build an engaged community that translates into paying clients. Our comprehensive management service takes full responsibility "
            "for your brand's presence across Facebook, Instagram, LinkedIn, and TikTok. We handle content ideation, copywriting, graphic design, "
            "scheduled publishing, proactive comment reply moderation, and monthly performance reporting."
        ),
        "benefits": (
            "Consistent High-Impact Publishing maintaining active brand top-of-mind awareness\n"
            "Proactive Community Moderation: Prompt responses to comments and buyer DMs\n"
            "Cross-Platform Distribution optimized specifically for each network's algorithm\n"
            "Strategic Audience Growth attracting qualified local and international followers\n"
            "Hashtag & Keyword Research expanding organic reach beyond your existing followers\n"
            "Transparent Monthly Growth Reports showing follower, reach, and inquiry growth"
        ),
        "process": (
            "1. Brand Voice & Audience Audit: Analyzing current engagement, target buyers, and competitors\n"
            "2. Content Strategy & Pillars Definition: Structuring educational, social proof, and sales pillars\n"
            "3. Monthly Content Production: Creating custom graphics, copy, and video reels\n"
            "4. Scheduled Publishing: Distributing posts during peak audience activity windows\n"
            "5. Community Management: Monitoring mentions, replying to comments, and routing inquiries\n"
            "6. Monthly Performance Review: Reviewing KPIs and refining content strategy"
        ),
        "image_url": "https://images.unsplash.com/photo-1533750516457-a7f992034fec?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Facebook Marketing",
        "icon_name": "thumb_up",
        "short_description": "Targeted Facebook community building, high-converting organic posts, customer groups cultivation, and local business customer acquisition.",
        "overview": (
            "Harness the massive scale of Facebook to drive reliable customer inquiries. We optimize your Facebook Page, "
            "curate viral engagement posts, publish customer case studies, establish interactive customer groups, "
            "and deploy local marketing strategies that generate consistent inquiries from your exact geographic target market."
        ),
        "benefits": (
            "Massive Reach across the world's largest social network and local demographic groups\n"
            "Facebook Group Community Management creating a loyal tribe of brand advocates\n"
            "Conversion-Focused Post Copywriting engineered to drive comments and direct inquiries\n"
            "Integrated Event & Product Launches maximizing attendance and early-bird sales\n"
            "Local Community Group Syndication sharing expertise in targeted regional groups\n"
            "Optimized Messenger Routing directing questions to your sales team's WhatsApp"
        ),
        "process": (
            "1. Facebook Page Health Audit: Optimizing cover, pinned posts, tabs, and bio\n"
            "2. Content Calendar Scheduling: Mixing video, carousel, and text-based discussion starters\n"
            "3. Visual Asset Creation: Designing Facebook-optimized high-contrast image graphics\n"
            "4. Group Engagement Strategy: Building or participating in high-value niche discussions\n"
            "5. Messenger Lead Capture Setup: Configuring automated FAQs and chat greetings\n"
            "6. Reach Analytics Monitoring: Analyzing post engagement and follower conversion"
        ),
        "image_url": "https://images.unsplash.com/photo-1562577309-4932fdd64cd1?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Instagram Marketing",
        "icon_name": "photo_camera",
        "short_description": "High-aesthetic Instagram feed curation, viral Reels creation, interactive Story funnels, and customer conversion funnels.",
        "overview": (
            "Turn your Instagram into an aspirational digital showroom. We engineer cohesive visual grid aesthetics, "
            "produce high-retention short-form video Reels, design interactive daily Stories with polls and question stickers, "
            "and build seamless link-in-bio funnels that funnel high-intent followers directly into booked consultations."
        ),
        "benefits": (
            "Curated High-End Visual Feed reflecting premium brand positioning and trust\n"
            "Viral Short-Form Reels engineered with trending audio to reach non-followers\n"
            "Daily Interactive Stories maintaining daily engagement and warm conversations\n"
            "Permanent Story Highlights acting as a mobile website for reviews, pricing, and FAQs\n"
            "Optimized Link-in-Bio Funnel directing traffic to WhatsApp, quotes, and shop pages\n"
            "Direct Message Lead Generation converting story viewers into paying clients"
        ),
        "process": (
            "1. Visual Identity & Grid Planning: Designing a signature 9-grid aesthetic pattern\n"
            "2. Reels Strategy & Scripting: Identifying trending formats, hooks, and call-to-actions\n"
            "3. Graphics & Video Production: Designing carousels, infographics, and motion assets\n"
            "4. Story Highlights Architecture: Organizing Social Proof, Services, and Contact highlights\n"
            "5. Bio & Link-in-Bio Optimization: Configuring custom mobile menu link trees\n"
            "6. Metric Evaluation: Tracking profile visits, website clicks, and DM inquiry volume"
        ),
        "image_url": "https://images.unsplash.com/photo-1611262588024-d12430b98920?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "TikTok Marketing",
        "icon_name": "smart_display",
        "short_description": "Trend-jacking short-form video strategies, TikTok algorithm optimization, brand challenges, and Gen Z/millennial conversion.",
        "overview": (
            "Unlock exponential organic reach on the world's fastest-growing entertainment platform. We craft high-energy TikTok video scripts, "
            "leverage trending sounds and algorithm-friendly hooks, showcase behind-the-scenes business operations, and create relatable educational content "
            "that captures attention and drives thousands of viewers to your bio link."
        ),
        "benefits": (
            "Unrivaled Organic Reach potential reaching hundreds of thousands of organic viewers\n"
            "Authentic Brand Humanization building deep emotional connections with modern buyers\n"
            "Algorithm-Optimized Hooks & Pacing ensuring high completion rates and FYP syndication\n"
            "Behind-the-Scenes Storytelling showcasing your expertise, packaging, and team\n"
            "Seamless Bio Traffic Routing directing viral viewers to your WhatsApp or store\n"
            "Trend Capitalization: Fast execution on viral formats before competitors notice"
        ),
        "process": (
            "1. TikTok Niche & Competitor Audit: Identifying viral video formats in your industry\n"
            "2. Scriptwriting & Hook Engineering: Writing high-retention 15-to-45 second video scripts\n"
            "3. Audio & Hashtag Curation: Matching scripts with trending sounds and SEO keywords\n"
            "4. Video Editing & Captions: Formatting fast-paced cuts, on-screen text, and captions\n"
            "5. Profile Bio & Link Setup: Adding direct inquiry links and business categories\n"
            "6. Retention Analytics Analysis: Analyzing watch-time graphs and follower conversion"
        ),
        "image_url": "https://images.unsplash.com/photo-1598128558393-70ff2141913f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "LinkedIn Marketing",
        "icon_name": "work",
        "short_description": "Executive thought leadership positioning, B2B corporate lead generation, and decision-maker direct messaging pipelines.",
        "overview": (
            "Win high-ticket corporate contracts and establish industry authority. We optimize personal executive profiles and corporate LinkedIn pages, "
            "publish data-backed industry thought leadership articles, produce professional PDF carousels, "
            "and execute targeted B2B networking campaigns that place you directly in front of CEOs, procurement heads, and key decision-makers."
        ),
        "benefits": (
            "High-Ticket B2B Lead Generation connecting with corporate decision-makers\n"
            "Executive Authority Positioning establishing founders as recognized industry leaders\n"
            "Engaging PDF Slide Carousels achieving high dwell time and document downloads\n"
            "Optimized LinkedIn Company Page showcasing corporate milestones, culture, and services\n"
            "Targeted InMail & Connection Sequences initiating warm corporate sales conversations\n"
            "Recruitment & Talent Attraction elevating your employer brand in the market"
        ),
        "process": (
            "1. Executive Profile Optimization: Rewriting headline, about section, and featured media\n"
            "2. Thought Leadership Content Roadmap: Outlining weekly case studies and industry insights\n"
            "3. Document Carousel Creation: Designing multi-slide professional PDF presentation decks\n"
            "4. Strategic Network Expansion: Identifying and connecting with verified decision-makers\n"
            "5. Corporate Page Management: Publishing company updates, press releases, and hiring news\n"
            "6. Pipeline Review: Tracking inbound inquiries and corporate RFP opportunities"
        ),
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Social Media Content Creation",
        "icon_name": "article",
        "short_description": "Persuasive copy, video scripts, multi-slide educational carousels, and infographics engineered for maximum shares and saves.",
        "overview": (
            "Stop posting generic filler content that gets ignored. We research, write, and produce high-value content engineered "
            "to solve your customers' real problems. Deliverables include deeply researched educational carousels, engaging video scripts, "
            "persuasive caption copywriting with irresistible calls-to-action, and actionable infographics that get saved and shared."
        ),
        "benefits": (
            "High-Save & High-Share Content that algorithms love and amplify organically\n"
            "Persuasive Sales Copywriting that overcomes customer skepticism and objections\n"
            "Educational Authority Building demonstrating your deep industry expertise\n"
            "Multi-Slide Visual Carousels breaking down complex topics into digestible steps\n"
            "Platform-Tailored Copy matching the unique culture of LinkedIn, IG, and Facebook\n"
            "Compelling Calls-to-Action guiding readers to comment, message, or visit your website"
        ),
        "process": (
            "1. Audience Pain Points Research: Identifying the top questions and hesitations of buyers\n"
            "2. Content Matrix Ideation: Brainstorming content across Trust, Education, and Offer pillars\n"
            "3. Drafting & Copywriting: Crafting engaging hooks, body value, and clear closing CTAs\n"
            "4. Multi-Media Visual Styling: Formatting into graphic carousels, quotes, and video scripts\n"
            "5. Review & Client Approval: Presenting batches in an organized review dashboard\n"
            "6. Performance Iteration: Doubling down on the formats that generate the most inquiries"
        ),
        "image_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Social Media Graphics",
        "icon_name": "image",
        "short_description": "Striking bespoke visual assets, promotional banners, story templates, and animated feed graphics aligned with brand guidelines.",
        "overview": (
            "Capture user attention in fast-scrolling social media feeds with thumb-stopping graphic design. "
            "Our creative team designs custom branded social graphics, flash sale promotional banners, quote cards, "
            "event announcements, and motion graphic assets built with precise typography and high visual contrast."
        ),
        "benefits": (
            "Thumb-Stopping Visual Contrast cutting through crowded social media noise\n"
            "100% Brand Consistency adhering strictly to your corporate fonts, colors, and logos\n"
            "Multi-Format Deliverables optimized for square feeds (1:1), portraits (4:5), and stories (9:16)\n"
            "Promotional Flash Sale & Event Banners that trigger urgency and action\n"
            "Editable Canva or Figma Templates enabling your internal team to create quick posts\n"
            "High-Resolution Exporting provided in crisp, compression-proof web formats"
        ),
        "process": (
            "1. Brand Guidelines Review: Studying your color palettes, fonts, and visual motifs\n"
            "2. Concept & Layout Wireframing: Sketching visual hierarchies for maximum legibility\n"
            "3. Graphic Production: Designing vector illustrations, photo compositions, and typography\n"
            "4. Multi-Aspect Ratio Adaptation: Resizing designs for Feed, Stories, and Banner slots\n"
            "5. Quality Review: Checking mobile screen contrast and legibility tests\n"
            "6. Final Asset Delivery: Delivering organized PNG, JPG, and editable master templates"
        ),
        "image_url": "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Content Calendars",
        "icon_name": "date_range",
        "short_description": "Strategic 30-day and 90-day publishing schedules mapping promotional milestones, educational pillars, and industry events.",
        "overview": (
            "Eliminate daily guesswork with a proactive, organized publishing schedule. We architect custom 30-day and 90-day "
            "editorial content calendars that strategically map out national holidays, seasonal product promotions, educational value drops, "
            "customer testimonials, and flash sales for consistent, stress-free execution."
        ),
        "benefits": (
            "Complete Freedom from Daily Stress: Know exactly what is posting weeks in advance\n"
            "Strategic Promotional Alignment synchronizing social posts with business revenue goals\n"
            "Balanced Content Pillars ensuring you educate, entertain, and sell in optimal ratios\n"
            "Holiday & Event Capitalization: Never miss Black Friday, New Year, or industry holidays\n"
            "Collaborative Cloud Dashboard (Notion / Trello / Sheets) for easy team reviews\n"
            "Integrated Asset Links connecting each scheduled post directly to approved graphics"
        ),
        "process": (
            "1. Annual Business Goals Mapping: Reviewing upcoming launches, events, and seasonal peaks\n"
            "2. Content Ratio Strategy: Establishing the 4-1-1 publishing ratio (Value vs Pitch)\n"
            "3. Calendar Grid Construction: Populating dates with topics, hooks, and content formats\n"
            "4. Resource & Asset Assignment: Tagging copywriters and graphic designers to each date\n"
            "5. Management Review & Approval: Walking through the full schedule with your team\n"
            "6. Continuous Schedule Iteration: Updating future calendar blocks based on past metrics"
        ),
        "image_url": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Paid Social Media Advertising",
        "icon_name": "ads_click",
        "short_description": "High-ROI paid advertising campaigns across Meta, TikTok, and LinkedIn with audience retargeting and budget optimization.",
        "overview": (
            "Stop boosting posts randomly with zero measurable return. We architect full-funnel paid advertising campaigns across "
            "Facebook, Instagram, TikTok, and LinkedIn. From cold prospect acquisition to dynamic retargeting, "
            "we optimize budgets daily to maximize your return on ad spend (ROAS) and lower your customer acquisition cost (CAC)."
        ),
        "benefits": (
            "Predictable Customer Acquisition turning ad spend directly into profitable revenue\n"
            "Deep Behavioral Audience Targeting reaching high-income buyers and decision-makers\n"
            "Dynamic Retargeting Ads re-engaging visitors who abandoned your website or cart\n"
            "Rigorous A/B Creative Testing continuously testing headlines, videos, and CTAs\n"
            "Server-Side Conversion API Setup bypassing iOS tracking blockers for accurate data\n"
            "Transparent Weekly Performance Dashboards tracking exact cost per lead and ROAS"
        ),
        "process": (
            "1. Campaign Objective & Budget Definition: Establishing target CPA and monthly ad budget\n"
            "2. Pixel & Conversion API Setup: Ensuring bulletproof server tracking before spending $1\n"
            "3. Audience Research & Segmenting: Creating Custom Audiences, Lookalikes, and Interest stacks\n"
            "4. High-Converting Ad Creative Production: Writing direct-response copy and designing creatives\n"
            "5. Campaign Launch & Real-Time Monitoring: Managing bidding, placements, and frequency\n"
            "6. Scaling & Budget Allocation: Directing budget into top-performing winning ads"
        ),
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Facebook/Instagram Ads",
        "icon_name": "paid",
        "short_description": "Hyper-targeted Meta advertising campaigns utilizing custom lookalike audiences, pixel conversion tracking, and high-converting video creatives.",
        "overview": (
            "Dominate feeds and stories across Facebook and Instagram. We develop high-converting Meta advertising campaigns "
            "utilizing Meta's advanced AI bidding algorithms, broad targeting, Lookalike Audiences, and scroll-stopping video ads. "
            "Our campaigns are engineered to drive instant purchases, catalog sales, and high-intent WhatsApp inquiries."
        ),
        "benefits": (
            "Direct WhatsApp Click-to-Chat Ads opening conversations directly with buyers\n"
            "Custom Lookalike Audiences finding new customers identical to your best buyers\n"
            "Mobile-Optimized Story & Reel Ad Formats capturing full-screen attention\n"
            "Catalog Dynamic Product Ads showing the exact items shoppers viewed on your site\n"
            "Budget Optimization (CBO/Advantage+) automatically distributing funds to top ads\n"
            "Detailed Demographic Breakdown showing which age, gender, and city converts best"
        ),
        "process": (
            "1. Meta Business Manager Audit: Securing ad accounts, payment methods, and business pages\n"
            "2. Funnel Architecture: Setting up Top of Funnel (Prospecting) and Bottom of Funnel (Retargeting)\n"
            "3. High-Impact Creative Development: Developing short video hooks and visual carousels\n"
            "4. Ad Copywriting: Crafting emotional problem-solution copy that converts cold traffic\n"
            "5. Split-Testing Execution: Testing multiple creative variants to identify winners\n"
            "6. Weekly Optimization: Pruning high-cost ad sets and scaling profitable campaigns"
        ),
        "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Lead Generation Campaigns",
        "icon_name": "person_add",
        "short_description": "Direct lead capture funnels with native instant forms, automated CRM routing, and high-intent customer pre-qualification.",
        "overview": (
            "Fill your sales pipeline with pre-qualified, ready-to-buy prospects. We engineer dedicated lead generation funnels "
            "utilizing native Meta Instant Forms, interactive landing pages, and automated instant notifications. "
            "Inquiries are validated for phone number and budget before being instantly routed to your sales team's WhatsApp or CRM."
        ),
        "benefits": (
            "High Volume of Qualified Leads delivered directly to your sales reps daily\n"
            "Pre-Screening Custom Questions filtering out tire-kickers and low budgets\n"
            "Instant WhatsApp & Email Alert Triggers notifying your team within 60 seconds of a lead\n"
            "Auto-Populated Mobile Forms making submission effortless with zero typing friction\n"
            "Automated CRM Integration feeding leads into HubSpot, Zoho, or Google Sheets\n"
            "Automated Instant Autoresponder SMS/Email confirming receipt and setting expectations"
        ),
        "process": (
            "1. Ideal Customer Profile (ICP) Analysis: Defining exact buyer qualifications and budget criteria\n"
            "2. High-Value Lead Magnet Creation: Crafting compelling offers (Quotation, Guide, Audit, Discount)\n"
            "3. Instant Form Design: Designing multi-step qualification questions with privacy policy\n"
            "4. Webhook Automation Setup: Connecting Zapier/webhooks for instantaneous lead alerts\n"
            "5. Campaign Launch & Quality Check: Inspecting initial lead quality and tweaking questions\n"
            "6. Sales Close Rate Review: Collaborating with your sales team to optimize closing ratios"
        ),
        "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Social Media Page Optimization",
        "icon_name": "tune",
        "short_description": "Comprehensive audit and overhaul of handles, keyword-rich bios, visual headers, call-to-action buttons, and pinned posts.",
        "overview": (
            "Turn your social media profiles from passive business cards into active customer acquisition hubs. "
            "We conduct an in-depth audit and complete makeover of your Instagram, Facebook, LinkedIn, and TikTok profiles—optimizing "
            "searchable name fields, persuasive bio copy, link trees, branded highlight covers, and pinned authority showcase posts."
        ),
        "benefits": (
            "Social Search SEO: Rank at the top when customers search for your services on Instagram & TikTok\n"
            "Crystal-Clear Value Proposition in your bio that tells visitors why they must choose you\n"
            "Frictionless Call-to-Action Paths guiding viewers directly to call, book, or shop\n"
            "Branded Story Highlight Covers creating an organized, premium profile aesthetic\n"
            "Pinned Showcase Posts highlighting your best reviews, team, and flagship offerings\n"
            "Cross-Platform Verification Checklist preparing your accounts for official checkmarks"
        ),
        "process": (
            "1. Profile Visibility & SEO Audit: Reviewing current search keywords, bio clarity, and links\n"
            "2. Keyword-Rich Handle & Name Tuning: Embedding primary service keywords in your profile title\n"
            "3. Conversion Bio Copywriting: Writing concise, impactful 150-character value propositions\n"
            "4. Highlight Cover Design: Creating matching minimalist icon covers for key highlights\n"
            "5. Pinned Content Strategy: Crafting 3 pinned anchor posts that convert new visitors\n"
            "6. Link-in-Bio Setup: Installing a streamlined mobile landing page for your profile link"
        ),
        "image_url": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Competitor Analysis",
        "icon_name": "visibility",
        "short_description": "Deep-dive intelligence benchmarking competitors' top-performing ads, engagement strategies, content gaps, and pricing models.",
        "overview": (
            "Gain an unfair advantage in your market by uncovering exactly what is working for your competitors. "
            "We dissect your top 5 market rivals—analyzing their active paid ad creatives in the Meta and Google Ad Libraries, "
            "identifying their highest-engagement content formats, analyzing their pricing structures, and identifying gaps you can exploit."
        ),
        "benefits": (
            "Direct Visibility into Competitors' Paid Ads: See what creative hooks they spend money on\n"
            "Identification of Underserved Market Gaps that your business can immediately dominate\n"
            "Benchmarking Engagement & Growth Rates against real market competitors\n"
            "Pricing & Promotional Intelligence revealing competitor discount tactics and offers\n"
            "Content Strategy Inspiration without wasting time on trial-and-error experiments\n"
            "Strategic Executive Report with clear actionable recommendations for your team"
        ),
        "process": (
            "1. Competitor Selection: Identifying direct, indirect, and aspirational market rivals\n"
            "2. Ad Library Forensics: Pulling and analyzing all active paid ad creatives and landing pages\n"
            "3. Content Performance Audit: Evaluating top posts, posting frequency, and comment sentiment\n"
            "4. Offer & Pricing Breakdown: Mapping competitor service tiers, guarantees, and pricing\n"
            "5. SWOT & Gap Identification: Highlighting weak spots where competitors fail customers\n"
            "6. Strategic Action Playbook: Delivering an actionable battle plan to outperform competitors"
        ),
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "social-media-digital-marketing",
        "title": "Social Media Strategy",
        "icon_name": "psychology",
        "short_description": "Master growth roadmap defining brand tone of voice, audience buyer personas, content pillars, KPI targets, and conversion paths.",
        "overview": (
            "Transform your marketing from scattered random posts into an orchestrated revenue engine. "
            "We develop a master social media strategy document tailored to your business goals. "
            "Includes deep customer persona profiling, tone of voice guidelines, content pillars, channel-specific playbooks, "
            "crisis management protocols, and quarterly growth milestones."
        ),
        "benefits": (
            "Complete Strategic Clarity: A definitive blueprint for everyone on your marketing team\n"
            "Deep Buyer Persona Profiling uncovering emotional purchase drivers and objections\n"
            "Established Tone of Voice Guidelines ensuring consistent, professional communication\n"
            "Concrete Quarterly Growth KPIs tracking follower growth, engagement, and sales leads\n"
            "Omnichannel Distribution Playbook for Instagram, Facebook, LinkedIn, TikTok & X\n"
            "Crisis Communication Protocols protecting your brand reputation during PR incidents"
        ),
        "process": (
            "1. Discovery & Business Model Review: Aligning marketing strategy with company revenue targets\n"
            "2. Customer Journey Architecture: Mapping awareness, consideration, and purchase touchpoints\n"
            "3. Content Pillars & Thematic Mapping: Defining core themes (Authority, Proof, Education, Pitch)\n"
            "4. Platform Role Definition: Assigning distinct objectives to each social platform\n"
            "5. Workflow & Tool Recommendations: Recommending scheduling, analytics, and CRM software\n"
            "6. Strategy Presentation & Workshop: Walking your executive leadership through the roadmap"
        ),
        "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80"
    },

    # =========================================================================
    # 🎨 3. Graphic Design & Branding (18 Services)
    # =========================================================================
    {
        "category_slug": "graphic-design-branding",
        "title": "Logo Design",
        "icon_name": "brush",
        "short_description": "Memorable, modern, vector logo design with full copyright transfer, monochrome variations, and scalable print/web asset packs.",
        "overview": (
            "Your logo is the foundation of your company's visual identity. We craft timeless, memorable, and modern vector logos "
            "that represent your mission and resonate with high-value customers. You receive comprehensive file packs including full-color, "
            "black-and-white, horizontal, vertical, and icon-only variations in vector SVG, EPS, PDF, and high-DPI transparent PNGs."
        ),
        "benefits": (
            "100% Unique Vector Art crafted from scratch with full commercial ownership transfer\n"
            "Multi-Variant Asset Package: Horizontal, stacked, emblem, and app icon versions\n"
            "Full Color & Monochrome Variations for dark backgrounds, light backgrounds, and print\n"
            "Scalable Without Loss of Quality from tiny website favicons to massive roadside billboards\n"
            "Color Codes Provided (Pantone, CMYK, RGB, HEX) for absolute printing accuracy\n"
            "Complimentary Mockups showing how your logo looks on business cards, shirts, and signs"
        ),
        "process": (
            "1. Creative Brief & Discovery: Exploring brand values, industry positioning, and aesthetic preferences\n"
            "2. Conceptualization & Sketching: Brainstorming multiple distinct visual directions\n"
            "3. Vector Digitization: Refining the strongest concepts in Adobe Illustrator\n"
            "4. Presentation & Client Review: Presenting 3 distinct logo concepts in real-world mockups\n"
            "5. Revisions & Perfection: Polishing typography, kerning, and color balances\n"
            "6. Master Asset Handover: Delivering complete production-ready master vector file package"
        ),
        "image_url": "https://images.unsplash.com/photo-1626785774625-ddcddc3445e9?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Brand Identity Design",
        "icon_name": "auto_awesome",
        "short_description": "Cohesive corporate visual identity systems including color palettes, typography pairings, visual motifs, and brand rules.",
        "overview": (
            "Build a cohesive, premium brand experience across every client touchpoint. "
            "We architect complete corporate visual identity systems—curating distinctive primary and secondary color palettes, "
            "harmonious typography systems, supporting geometric patterns and iconography, and visual styling rules "
            "that make your business instantly recognizable."
        ),
        "benefits": (
            "Unmistakable Brand Recognition making your business look like an established market leader\n"
            "Harmonious Color Palette with psychological contrast engineered for digital and print\n"
            "Typography Hierarchy Pairings specifying primary heading, body, and accent fonts\n"
            "Bespoke Brand Patterns & Graphic Textures adding depth to your presentations and collateral\n"
            "Photography & Iconography Art Direction guiding all future visual content creation\n"
            "Elimination of Inconsistent Visuals across your website, social media, and printed flyers"
        ),
        "process": (
            "1. Brand Strategy Discovery: Defining brand archetype, personality, and audience perception\n"
            "2. Moodboard Curation: Assembling visual inspiration across texture, color, and typography\n"
            "3. Identity System Development: Creating the logo, color scales, and typography rules\n"
            "4. Collateral Application Testing: Applying identity across mock stationery, websites, and apparel\n"
            "5. Brand Guidelines Compilation: Documenting exact rules in an executive brand guide\n"
            "6. Asset Library Handover: Providing digital font files, color swatches, and vector elements"
        ),
        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Business Cards",
        "icon_name": "badge",
        "short_description": "Premium print-ready business cards featuring QR code vCard links, spot UV finish specifications, and executive typography.",
        "overview": (
            "Make an unforgettable first impression at meetings, expos, and networking events. "
            "We design luxury, executive business cards engineered with clean typography, dynamic QR codes linking to your digital vCard, "
            "and specialized printing specifications (spot UV gloss, gold foil stamping, matte velvet lamination, and embossed lettering)."
        ),
        "benefits": (
            "Executive Tactile Impression commanding respect in face-to-face negotiations\n"
            "Dynamic QR Code Integration allowing prospects to save your phone contact in 1 tap\n"
            "Print-Ready Vector Files with accurate 3mm bleed margins, crop marks, and CMYK color\n"
            "Specialized Finish Guides for printers (Spot UV, Embossing, Foil Stamping, Matte Lamination)\n"
            "Multi-Employee Layouts provided for leadership, sales representatives, and technicians\n"
            "Standard & Custom Sizing options (Standard 85x55mm, Square, or Rounded Corners)"
        ),
        "process": (
            "1. Information Architecture: Selecting essential contact details, handles, and addresses\n"
            "2. Layout & Typography Design: Designing front and back layouts aligned with brand rules\n"
            "3. QR Code Generation: Creating custom scannable vCard contact links\n"
            "4. Print Finish Specification: Designing separate layers for Spot UV, Emboss, or Foil\n"
            "5. Client Approval & Proofing: Reviewing 3D photorealistic mockups\n"
            "6. Printer-Ready Handover: Delivering high-DPI 300 DPI CMYK PDF files with bleeds"
        ),
        "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Letterheads",
        "icon_name": "description",
        "short_description": "Elegant corporate letterheads provided in print-ready PDF and editable Microsoft Word formats for daily official correspondence.",
        "overview": (
            "Bring corporate professionalism to every proposal, invoice, and formal letter. "
            "We design elegant corporate letterheads incorporating your logo, registration details, verified physical address, and contact information. "
            "Delivered both as high-resolution print-ready vector PDFs and fully editable Microsoft Word templates (.docx)."
        ),
        "benefits": (
            "Corporate Legitimacy for proposals, contracts, tenders, and official communications\n"
            "Fully Editable Microsoft Word Template: Type and print directly from your computer\n"
            "Print-Ready CMYK PDF Files for professional high-volume offset printing\n"
            "Matching Envelope & Continuation Sheet designs for multi-page documents\n"
            "Precise Grid Margins ensuring text never overlaps your corporate header or footer\n"
            "Digital PDF Letterhead format ready for sending official contracts via email"
        ),
        "process": (
            "1. Corporate Legal Information Collection: Gathering official names, pins, and addresses\n"
            "2. Header & Footer Layout Design: Balancing visual elegance with maximum writing space\n"
            "3. Vector PDF Production: Setting up CMYK 300 DPI layout with print bleed margins\n"
            "4. Microsoft Word Template Creation: Embedding protected header/footer in editable .docx\n"
            "5. Print & Digital Testing: Testing layout across desktop printers and PDF exports\n"
            "6. Final Delivery: Providing .docx, .pdf, and vector source assets"
        ),
        "image_url": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Company Profiles",
        "icon_name": "menu_book",
        "short_description": "Comprehensive corporate brochures showcasing mission, leadership, service capabilities, portfolio, and credentials for tenders.",
        "overview": (
            "Win high-value corporate tenders and institutional clients with an executive company profile. "
            "We write, design, and structure comprehensive multi-page corporate profiles (8 to 32 pages) "
            "highlighting your company history, executive leadership, core capabilities, past project case studies, client testimonials, and legal credentials."
        ),
        "benefits": (
            "Tender-Winning Corporate Document meeting all institutional procurement standards\n"
            "Professional Persuasive Copywriting communicating your unique value proposition\n"
            "High-End Visual Layout with corporate photography, infographics, and project showcases\n"
            "Dual Format Delivery: Lightweight digital PDF for email and high-DPI print-ready format\n"
            "Structured Sections: Vision, Mission, Core Team, Organogram, Services, and Testimonials\n"
            "Editable Master Files allowing your team to update project lists and team members in future"
        ),
        "process": (
            "1. Content & Questionnaire Intake: Gathering company achievements, certifications, and project lists\n"
            "2. Professional Copywriting & Proofreading: Structuring compelling corporate narrative\n"
            "3. Visual Wireframing: Designing master grids, typography hierarchies, and photo frames\n"
            "4. Page-by-Page Design: Crafting infographics, team profiles, and case study pages\n"
            "5. Executive Review & Revisions: Refining page counts and visual details with stakeholders\n"
            "6. Dual Publishing: Delivering interactive web PDF with clickable links and 300 DPI print files"
        ),
        "image_url": "https://images.unsplash.com/photo-1542744094-3a31727560fa?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Brochures",
        "icon_name": "auto_stories",
        "short_description": "High-impact bi-fold, tri-fold, and multi-page brochures engineered to explain complex services and convert trade show prospects.",
        "overview": (
            "Equip your sales team with persuasive physical and digital collateral. We design bi-fold, tri-fold, and gate-fold brochures "
            "that guide readers through your product or service benefits. Combining clean typography, captivating imagery, "
            "and strong calls-to-action, our brochures turn casual readers into active inquiries."
        ),
        "benefits": (
            "Structured Sales Narrative walking prospects step-by-step through your solutions\n"
            "Multiple Fold Formats: Bi-fold (4 pages), Tri-fold (6 panels), or Z-fold\n"
            "Dual Web & Print Delivery: Interactive web PDF plus commercial print-ready files\n"
            "Eye-Catching Front Covers commanding attention in display racks and trade shows\n"
            "Clear Contact & QR Sections directing readers to WhatsApp, phone, and websites\n"
            "Accurate CMYK Print Alignment ensuring folds fall cleanly between panels"
        ),
        "process": (
            "1. Format & Purpose Strategy: Selecting the right folding format for your service complexity\n"
            "2. Information Hierarchy Mapping: Allocating sections across front, interior, and back panels\n"
            "3. Copywriting & Value Bulleting: Writing punchy, scannable, benefit-rich text\n"
            "4. High-Resolution Layout Design: Balancing graphics, icons, and white space\n"
            "5. Fold Line Calibration: Verifying panel widths (e.g. inside flap adjustment on tri-folds)\n"
            "6. Print Production Delivery: Providing 300 DPI PDF files with crop marks and bleed"
        ),
        "image_url": "https://images.unsplash.com/photo-1586282391129-76a6df230234?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Flyers",
        "icon_name": "local_offer",
        "short_description": "Eye-catching promotional flyers for event marketing, product launches, flash sales, and direct street/inbox distribution.",
        "overview": (
            "Promote your events, special promotions, and product launches with high-energy promotional flyers. "
            "Designed in standard sizes (A5, A6, DL), our flyers combine bold headlines, vibrant color harmony, clear pricing, "
            "and scannable QR codes that drive immediate action from prospects."
        ),
        "benefits": (
            "High-Impact Visual Urgency driving fast customer response for promotions and events\n"
            "Single & Double-Sided Layouts maximizing marketing real estate and product details\n"
            "Cost-Effective Mass Distribution format ideal for door-to-door, in-store, and events\n"
            "Integrated Dynamic QR Codes turning paper flyers into direct digital WhatsApp chats\n"
            "Digital Social Media Flyer Variants included for WhatsApp status and Instagram sharing\n"
            "Commercially Certified Print Files ready for instant delivery to any print shop"
        ),
        "process": (
            "1. Promotion Goal & Hook Definition: Identifying the main offer, discount, or event date\n"
            "2. Layout Composition: Placing bold headline, featured product visual, and key benefits\n"
            "3. Call-to-Action & Contact Mapping: Adding clear phone, location, and QR scan badges\n"
            "4. Color & Contrast Balancing: Ensuring maximum legibility even in dim lighting\n"
            "5. Digital Format Generation: Exporting 1:1 and 9:16 crops for WhatsApp status and Instagram\n"
            "6. Print Delivery: Delivering print-ready CMYK PDFs with standard 3mm bleed"
        ),
        "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Posters",
        "icon_name": "aspect_ratio",
        "short_description": "Large-format indoor and outdoor promotional posters with crisp typography and striking visual compositions.",
        "overview": (
            "Command attention across storefronts, convention centers, and billboards. "
            "We design large-format posters (A3, A2, A1, A0) with ultra-sharp vector graphics, high-resolution imagery, "
            "and powerful typographic hierarchy that can be read clearly from distances of 10 meters or more."
        ),
        "benefits": (
            "High-Visibility Impact readable from across a room or busy street\n"
            "Large-Scale Vector Precision preventing pixelation or blurriness at large sizes\n"
            "Strong Typographic Hierarchy guiding the viewer's eye from headline to details\n"
            "Vibrant Color Saturation engineered for outdoor sunlight and commercial display lighting\n"
            "Versatile Application: Retail windows, educational seminars, movie/music events, and trade shows\n"
            "Print-Certified Files delivered with correct color profiles for large-format plotters"
        ),
        "process": (
            "1. Sizing & Viewing Distance Calculation: Choosing A3 to A0 dimensions and focal points\n"
            "2. Concept & Visual Hero Selection: Selecting or creating a singular commanding visual asset\n"
            "3. Typographic Composition: Setting headline, date/venue, and sponsor logos in clear tiers\n"
            "4. Color Calibration for Print: Ensuring deep blacks and saturated hues in CMYK\n"
            "5. Proofing & Distance Legibility Checks: Simulating multi-meter viewing clarity\n"
            "6. Production File Export: Supplying uncompressed TIFF and PDF master files"
        ),
        "image_url": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Banners",
        "icon_name": "view_carousel",
        "short_description": "High-resolution digital and vinyl display banners for trade shows, website headers, billboards, and storefront signage.",
        "overview": (
            "Make your brand impossible to ignore at expos, roadside billboards, and digital websites. "
            "We design custom horizontal and vertical vinyl banners with eyelets, digital website hero banners, "
            "and large outdoor billboards tailored to withstand printing scaling and outdoor viewing conditions."
        ),
        "benefits": (
            "Massive Outdoor & Indoor Brand Presence commanding immense visibility\n"
            "Engineered Eyelet & Hem Margins ensuring text is never punctured by grommets\n"
            "Ultra-Durable Vector Artwork sharp at 10+ meter billboard dimensions\n"
            "Digital Website Header Banners included for your homepage and promotional landing pages\n"
            "Weather-Proof Color Formulation specifications for UV-resistant vinyl printing\n"
            "Fast Turnaround Times meeting strict event and exhibition deadlines"
        ),
        "process": (
            "1. Dimension & Installation Audit: Reviewing exact length, height, and mounting method\n"
            "2. Safe Zone & Eyelet Margin Setup: Marking 5cm safety margins around all edges\n"
            "3. Bold Headline & Visual Composition: Crafting an instantly understandable message\n"
            "4. Sponsor & Contact Placement: Positioning logos and phone numbers for rapid recall\n"
            "5. Color Matching & DPI Scaling: Scaling resolution for large-format industrial printers\n"
            "6. Print Production Handover: Delivering print-ready files with trim and grommet guides"
        ),
        "image_url": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Roll-up Banners",
        "icon_name": "view_day",
        "short_description": "Standout retractable pull-up banners for corporate expos, conferences, retail showrooms, and hotel foyer displays.",
        "overview": (
            "The essential portable marketing display for every exhibition and conference. "
            "We design vertical pull-up retractable banners (standard 85x200cm, 100x200cm, and 120x200cm) "
            "engineered with eye-level headlines, bulleted service highlights, high-resolution photography, and clear base contact details."
        ),
        "benefits": (
            "Eye-Level Ergonomic Design placing your logo and core message at natural eye height (150-180cm)\n"
            "Portable Professional Showcase for trade shows, retail showrooms, and hotel summits\n"
            "Clear Base Margin Compensation ensuring bottom contact info isn't hidden inside the cassette\n"
            "Bulleted Service Breakdown making your key competitive advantages readable in 3 seconds\n"
            "High-Resolution 300 DPI Vector Artwork ensuring crisp logo, icons, and text\n"
            "Print-Ready Files with Bleed ready to submit directly to your banner hardware supplier"
        ),
        "process": (
            "1. Cassette Hardware Sizing: Confirming standard 85x200cm or custom width with printer\n"
            "2. Top/Bottom Safe Area Setup: Accounting for top hanger clamp and bottom cassette roll-in\n"
            "3. Eye-Level Headline Layout: Positioning primary brand mark and value proposition at eye level\n"
            "4. Body Deliverables Composition: Structuring 4-6 concise bullet points with custom icons\n"
            "5. Contact & Social Proof Footer: Adding web, phone, and QR details above the base line\n"
            "6. Production Delivery: Exporting 150-300 DPI CMYK PDF with 50mm bottom bleed"
        ),
        "image_url": "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Product Catalogues",
        "icon_name": "collections_bookmark",
        "short_description": "Comprehensive multi-page digital and print product catalogues featuring pricing tables, SKU details, and high-res imagery.",
        "overview": (
            "Empower wholesale buyers and retail clients to browse and order your full product inventory. "
            "We design structured, multi-page product catalogues (12 to 100+ pages) with consistent grid layouts, "
            "clear category divider spreads, SKU numbering, specifications, pricing matrices, and clickable digital PDF links."
        ),
        "benefits": (
            "Structured Wholesale & Retail Ordering tool making bulk purchasing effortless\n"
            "Consistent Multi-Page Grid Architecture maintaining visual harmony across 100+ items\n"
            "Interactive Digital PDF Format with clickable table of contents and order links\n"
            "SKU, Dimensions & Specifications Tables eliminating customer ordering errors\n"
            "Category Divider Spreads providing clean visual pacing between product lines\n"
            "Print-Ready Booklet PDF files with saddle-stitch or perfect-binding margin allowances"
        ),
        "process": (
            "1. Catalog Structure & Product Matrix: Organizing categories, product names, SKUs, and prices\n"
            "2. Master Page Template Design: Crafting uniform product card grids, headers, and footers\n"
            "3. Product Batch Population: Placing high-res photos, descriptions, and specification tables\n"
            "4. Table of Contents & Indexing: Generating page numbers and category divider pages\n"
            "5. Interactive Link Insertion: Linking product items to website checkout and WhatsApp\n"
            "6. Print & Digital Export: Delivering web-optimized digital PDF and high-res CMYK print files"
        ),
        "image_url": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Restaurant Menus",
        "icon_name": "restaurant",
        "short_description": "Appetizing laminated and leather-bound menu designs engineered using menu engineering psychology to highlight high-margin dishes.",
        "overview": (
            "Increase your restaurant or bar's average check size through strategic menu engineering. "
            "We design mouthwatering, durable restaurant menus that apply visual eye-movement psychology—placing "
            "high-margin signature dishes in primary focal areas, organizing clear dish categories, and using elegant typography."
        ),
        "benefits": (
            "Menu Engineering Psychology proven to increase high-margin dish sales by 15-20%\n"
            "Mouthwatering Layout & Typography designed to enhance perceived culinary quality\n"
            "Durable Print Specifications for synthetic waterproof paper or leather jacket inserts\n"
            "Organized Categorization (Appetizers, Mains, Cocktails, Desserts) for effortless browsing\n"
            "Dietary Iconography Badges (Vegetarian, Gluten-Free, Chef Signature, Spicy)\n"
            "Matching Digital Mobile Menu version included for QR code table scanning"
        ),
        "process": (
            "1. Dish Profitability Audit: Identifying your highest-margin dishes for strategic placement\n"
            "2. Layout & Format Sizing: Selecting single sheet, A4 bi-fold, or booklet dimensions\n"
            "3. Typographic Hierarchy & Price Styling: Formatting prices without currency symbols to reduce price sensitivity\n"
            "4. Photography & Texture Integration: Retouching hero dish imagery and backdrop textures\n"
            "5. Proofreading & Allergen Tagging: Verifying ingredients, spelling, and allergen icons\n"
            "6. Print Production Delivery: Delivering waterproof print files with protective laminate bleed"
        ),
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "QR Code Menus",
        "icon_name": "qr_code_scanner",
        "short_description": "Branded table-top cards, acrylic stands, and digital menu landing pages with instant touchless smartphone scanning.",
        "overview": (
            "Elevate your hospitality brand with sleek, touchless table QR menus. "
            "We design branded acrylic table-talker inserts, wooden table blocks, and durable vinyl stickers featuring your logo, "
            "clear scan instructions, Wi-Fi login credentials, and a high-speed mobile digital menu interface."
        ),
        "benefits": (
            "Touchless Modern Dining Experience beloved by tech-savvy customers\n"
            "Branded Table-Talker Graphic Designs matching your restaurant's interior aesthetic\n"
            "Wi-Fi & Social Media Prompt Integration encouraging customers to follow on Instagram\n"
            "Zero Waiter Bottlenecks: Diners can view specials the moment they sit down\n"
            "Durable Waterproof Print Specifications for table-top acrylic and sticker materials\n"
            "Dynamic QR Link Infrastructure allowing you to edit menu URLs without reprinting"
        ),
        "process": (
            "1. Table Display Hardware Review: Selecting acrylic stands, wooden blocks, or table stickers\n"
            "2. Custom QR Generation: Embedding your restaurant logo into scannable vector QR codes\n"
            "3. Card & Stand Layout Design: Designing front and back table-talker graphics with instructions\n"
            "4. Camera Readability Testing: Verifying scan speed under dim candlelight and ambient lighting\n"
            "5. Table Number Personalization: Numbering stands for direct table delivery (optional)\n"
            "6. Print File Delivery: Delivering high-DPI PDF files formatted for acrylic manufacturers"
        ),
        "image_url": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Certificates",
        "icon_name": "workspace_premium",
        "short_description": "Formal academic and corporate certificates of completion, excellence, and appreciation with security guilloche border details.",
        "overview": (
            "Honor achievements and issue prestigious credentials that recipients proudly frame and share online. "
            "We design luxury academic, training, and corporate certificates of completion featuring intricate guilloche security borders, "
            "metallic foil stamp accents, official signature lines, and serial number tracking fields."
        ),
        "benefits": (
            "Prestigious Corporate Aesthetic that students and attendees are proud to display on LinkedIn\n"
            "Intricate Security Guilloche Borders deterring counterfeit reproduction\n"
            "Dual Print & Digital Delivery: Print-ready vector PDFs plus editable mail-merge templates\n"
            "Foil Stamp & Emboss Layer Specifications for gold, silver, or bronze metallic seals\n"
            "Pre-Configured Signature Lines for Directors, Principals, and Award Committees\n"
            "Standard A4 and US Letter Formats ready for commercial certificate cardstock"
        ),
        "process": (
            "1. Award Purpose & Hierarchy: Establishing certificate title, recipient field, and award citation\n"
            "2. Security Border & Guilloche Design: Constructing intricate geometric vector border patterns\n"
            "3. Typographic Layout: Pairing classic serif display fonts with elegant script accents\n"
            "4. Signature & Seal Configuration: Placing official seal badge and authorized signature lines\n"
            "5. Variable Data Setup: Creating editable fields for automated name batch printing\n"
            "6. Production Delivery: Supplying 300 DPI print-ready files and editable templates"
        ),
        "image_url": "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Social Media Designs",
        "icon_name": "design_services",
        "short_description": "High-impact Canva and Figma post packs, banner headers, highlight covers, and editable templates for corporate branding.",
        "overview": (
            "Empower your internal team to publish polished on-brand social media posts every single day. "
            "We build comprehensive branded template systems in Figma and Canva—including quote layouts, product spotlight templates, "
            "customer review cards, carousel slides, and announcement banners pre-formatted with your fonts, colors, and logos."
        ),
        "benefits": (
            "Reusable Editable Templates in Canva or Figma: Update text and photos in 60 seconds\n"
            "100% Brand Consistency ensuring every team member stays strictly on-brand\n"
            "Comprehensive Pack (30+ Designs): Quotes, case studies, product drops, and testimonials\n"
            "Multi-Platform Dimensions: Square (1080x1080), Portrait (1080x1350), and Story (1080x1920)\n"
            "Pre-Loaded Font & Color Kits configured directly in your team's Canva Brand Kit\n"
            "Video Walkthrough Tutorial teaching your staff how to edit and export graphics easily"
        ),
        "process": (
            "1. Brand Kit Audit: Collecting official logos, color codes, and web fonts\n"
            "2. Content Types Mapping: Identifying the top 10 recurring post formats you publish\n"
            "3. Template Architecture in Figma/Canva: Designing flexible, modular graphic layouts\n"
            "4. Multi-Size Adaptation: Resizing templates across Post, Story, and Banner canvas sizes\n"
            "5. Video Training Recording: Recording a 10-minute loom video showing how to customize\n"
            "6. Team Access Transfer: Sharing editable Canva/Figma master link with full edit rights"
        ),
        "image_url": "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Advertisements",
        "icon_name": "featured_video",
        "short_description": "Print magazine ads, newspaper layouts, digital billboards, and display network creatives that drive immediate customer action.",
        "overview": (
            "Maximize the return on your print and outdoor advertising investments. We design high-conversion full-page, "
            "half-page, and strip advertisements for business magazines, industry journals, national newspapers, and digital LED billboards. "
            "Every ad is engineered with a compelling hook, proof-driven body copy, and trackable call-to-action."
        ),
        "benefits": (
            "High-Impact Advertising Design that commands reader attention on glossy magazine pages\n"
            "Direct-Response Principles applied to print: Clear hook, problem-solution, and strong CTA\n"
            "Strict Ad Specification Compliance adhering to exact publisher trim, bleed, and DPI specs\n"
            "Unique QR Code Tracking measuring exact phone calls and scans from physical print ads\n"
            "High-DPI CMYK Color Separation ensuring rich, vibrant ink rendering on newsprint or gloss\n"
            "Digital Display Ad Pack variants included for Google Display Network and web banners"
        ),
        "process": (
            "1. Publisher Specification Review: Obtaining exact mechanical trim, bleed, and safe area dimensions\n"
            "2. Creative Concept & Copywriting: Crafting an arresting headline and problem-focused pitch\n"
            "3. Visual Hierarchy Layout: Placing hero product imagery, customer quote, and offer\n"
            "4. Dedicated Tracking Setup: Generating a trackable QR code and custom landing page URL\n"
            "5. Pre-Press Flight Check: Checking color density, font embedding, and 300 DPI resolution\n"
            "6. Publisher Direct Delivery: Supplying certified PDF/X-1a files directly to the media house"
        ),
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Packaging Design",
        "icon_name": "inventory",
        "short_description": "Shelf-ready product box designs, pouch labels, bottle sleeves, and custom packaging dies that capture retail buyers.",
        "overview": (
            "Stand out on crowded retail shelves and deliver an unforgettable unboxing experience. "
            "We design commercial packaging—including folding carton boxes, stand-up pouch bags, cosmetic bottle labels, "
            "can wraps, and corrugated shipping mailers. Includes exact dieline precision, barcode integration, and legal compliance."
        ),
        "benefits": (
            "High Shelf-Impact Design engineered to win retail buyer attention against competitors\n"
            "Exact Dieline Precision calibrated to your manufacturer's technical cutting templates\n"
            "Regulatory Compliance: Ingredients list, barcode (EAN/UPC), batch, and recycling icons\n"
            "Special Print Finish Layers: Spot UV, gold hot-foil stamping, embossing, and soft-touch matte\n"
            "3D Photorealistic Packaging Mockups for pitch decks, social media, and e-commerce stores\n"
            "Complete Production-Ready Vector Files ready for immediate industrial printing"
        ),
        "process": (
            "1. Manufacturer Dieline Intake: Obtaining exact CAD dieline template from your packaging supplier\n"
            "2. Retail Category & Shelf Research: Analyzing competitor packaging in target supermarkets\n"
            "3. Front Panel Hierarchy Design: Placing brand, product name, weight, and key differentiator\n"
            "4. Regulatory Back Panel Layout: Formatting ingredients, nutritional tables, and barcodes\n"
            "5. 3D Packaging Render Generation: Rendering realistic 3D bottle/box mockups for marketing\n"
            "6. Industrial Print Handover: Delivering layered vector Illustrator files with separate die lines"
        ),
        "image_url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "graphic-design-branding",
        "title": "Brand Guidelines",
        "icon_name": "import_contacts",
        "short_description": "Comprehensive brand rulebook specifying logo clear space, typography hierarchy, primary/secondary colors, and brand voice.",
        "overview": (
            "Protect and scale your visual identity across any future agency, contractor, or internal hire. "
            "We compile an executive 20-to-40 page Corporate Brand Identity Guidelines manual (Brand Style Guide) "
            "documenting logo minimum sizing and clear space, prohibited logo uses, color codes (HEX, RGB, CMYK, Pantone), "
            "typography pairings, photography style rules, and corporate voice."
        ),
        "benefits": (
            "Absolute Brand Consistency across all future marketing campaigns, designers, and vendors\n"
            "Strict Logo Usage Rules: Defining clear space, minimum size, and prohibited distortions\n"
            "Exact Color Formulations: Precise CMYK (print), HEX (web), and Pantone (offset) values\n"
            "Typography Rules: Defining primary, secondary, and web-safe fallback font hierarchies\n"
            "Imagery & Tone of Voice Guidelines establishing how your brand speaks and photographs\n"
            "Executive Reference PDF delivered to onboard new staff and external marketing agencies"
        ),
        "process": (
            "1. Brand Identity Compilation: Gathering all final logo assets, color palettes, and fonts\n"
            "2. Logo Rules Formulation: Calculating clear space formulas and minimum reproduction sizes\n"
            "3. Color System Documentation: Testing and listing exact CMYK, RGB, HEX, and Pantone codes\n"
            "4. Typography Spec Sheets: Setting leading, tracking, and font licensing instructions\n"
            "5. Brand In Action Mockups: Demonstrating correct application on uniforms, cars, and collateral\n"
            "6. Master PDF Compilation: Exporting interactive, beautifully typeset executive Brand Manual"
        ),
        "image_url": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=800&q=80"
    },

    # =========================================================================
    # 📊 4. Analytics & Business Intelligence (12 Services)
    # =========================================================================
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Google Analytics",
        "icon_name": "query_stats",
        "short_description": "Complete Google Analytics 4 (GA4) configuration with custom conversion event tracking, user funnels, and e-commerce revenue reporting.",
        "overview": (
            "Stop operating in the dark. We configure enterprise Google Analytics 4 (GA4) with custom event tracking via Google Tag Manager (GTM). "
            "Track every critical customer action—button clicks, form submissions, video plays, WhatsApp inquiries, and e-commerce transactions—with "
            "custom audience segmentations, user retention cohorts, and automated monthly executive reports."
        ),
        "benefits": (
            "Full Visibility into Every Website Visitor: Traffic sources, user devices, and top pages\n"
            "Custom Conversion Event Tracking for form submissions, WhatsApp clicks, and phone calls\n"
            "Enhanced E-Commerce Tracking recording product views, cart additions, and net revenue\n"
            "Google Tag Manager (GTM) Architecture eliminating the need for developer code changes\n"
            "Cross-Domain Tracking tracking users seamlessly between landing pages and main sites\n"
            "Automated Monthly Executive Email Reports delivered directly to leadership inboxes"
        ),
        "process": (
            "1. Measurement Strategy & KPI Definition: Defining key business goals and micro-conversions\n"
            "2. Google Tag Manager Container Deployment: Installing clean, asynchronously loading GTM container\n"
            "3. Custom Trigger & Tag Configuration: Setting up tracking for button clicks, forms, and WhatsApp\n"
            "4. GA4 Property Hardening: Filtering internal office IP traffic and extending data retention to 14 months\n"
            "5. Conversion Funnel Setup: Building step-by-step funnel visualization reports\n"
            "6. Data Validation: Verifying real-time debug view and publishing container live"
        ),
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Search Console Analytics",
        "icon_name": "troubleshoot",
        "short_description": "Deep-dive Google Search Console audits, indexing issue resolution, keyword impression tracking, and organic click-through rate tuning.",
        "overview": (
            "Unlock what Google really thinks about your website. We connect and optimize Google Search Console (GSC) to track your organic keyword rankings, "
            "identify crawling and mobile indexing errors, analyze search impressions vs. clicks, submit XML sitemaps, and fix Core Web Vitals issues "
            "that prevent your website from ranking on page 1 of Google."
        ),
        "benefits": (
            "Exact Organic Search Keyword Data: See which Google queries bring real visitors to your site\n"
            "Identification & Repair of Indexing Errors: Fix 404s, redirect loops, and crawl blocks\n"
            "Click-Through Rate (CTR) Optimization: Identify keywords ranking well but lacking clicks\n"
            "XML Sitemap Validation & Submission ensuring new pages are indexed within hours\n"
            "Core Web Vitals & Mobile Usability Alerts warning of real-world user experience flaws\n"
            "Security & Manual Penalty Monitoring ensuring your domain is protected from Google penalties"
        ),
        "process": (
            "1. Domain Verification: Verifying domain ownership via DNS TXT record for full-domain coverage\n"
            "2. Technical Coverage & Indexing Audit: Identifying excluded, no-index, and 404 error pages\n"
            "3. XML Sitemap & Robots.txt Tuning: Submitting dynamic sitemaps and removing crawl blocks\n"
            "4. Query & Page Performance Deep Dive: Grouping keywords by search intent and CTR opportunity\n"
            "5. Title & Meta Optimization Recommendations: Rewriting low-CTR search snippets\n"
            "6. Monthly Rank Progression Reporting: Tracking average position shifts and total clicks"
        ),
        "image_url": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Website Performance Reports",
        "icon_name": "speed",
        "short_description": "Core Web Vitals optimization reports, server response audits, mobile usability reviews, and bottleneck elimination benchmarks.",
        "overview": (
            "Slow websites lose sales and get penalized by Google. We perform comprehensive technical audits analyzing Core Web Vitals "
            "(Largest Contentful Paint, Cumulative Layout Shift, Interaction to Next Paint), server Time to First Byte (TTFB), "
            "unoptimized images, render-blocking JavaScript, and database query bottlenecks with actionable code recommendations."
        ),
        "benefits": (
            "Actionable Technical Speed Audit scoring your site on Google PageSpeed Insights\n"
            "Core Web Vitals Benchmarking: Optimize LCP, CLS, and INP metrics for green scores\n"
            "Server TTFB & Response Analysis identifying slow hosting or unoptimized database queries\n"
            "Image & Asset Compression Audit discovering oversized PNGs slowing mobile downloads\n"
            "Third-Party Script Impact Review tracking the drag caused by analytics, chats, and tracking tags\n"
            "Priority Fix Checklist ranking optimizations from highest ROI to lowest effort"
        ),
        "process": (
            "1. Multi-Device Benchmark Testing: Running diagnostic audits across mobile 4G and desktop fiber\n"
            "2. Core Web Vitals Deep-Dive: Measuring exact seconds and milliseconds of layout shift and paint\n"
            "3. Code & Asset Bloat Inspection: Identifying unused CSS, heavy JS libraries, and render blocks\n"
            "4. Database & Server Profiling: Inspecting server response times and caching hit ratios\n"
            "5. Report Compilation: Compiling an executive summary and detailed developer action plan\n"
            "6. Optimization Walkthrough: Consulting with your team to review and implement speed fixes"
        ),
        "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Social Media Analytics",
        "icon_name": "trending_up",
        "short_description": "Multi-platform performance tracking analyzing engagement rate, follower retention, reach trends, and paid conversion attribution.",
        "overview": (
            "Turn social media data into clear strategic direction. We aggregate and analyze metrics across your Instagram, Facebook, "
            "TikTok, LinkedIn, and YouTube channels. Our analytics reports uncover which content formats generate genuine buyer inquiries, "
            "audience demographic shifts, optimal posting windows, and conversion attribution paths."
        ),
        "benefits": (
            "Unified Cross-Platform Dashboard combining data from IG, Facebook, TikTok & LinkedIn\n"
            "True Engagement Rate Benchmarking cutting through vanity follower counts\n"
            "Content Type ROI Ranking: Discover whether Reels, Carousels, or Single Posts drive revenue\n"
            "Audience Demographic Intelligence revealing age, gender, and top active geographical cities\n"
            "Optimal Posting Time Algorithms based on your specific audience's real activity peaks\n"
            "Monthly Executive PDF Scorecards with clear strategic guidance for next month's content"
        ),
        "process": (
            "1. Account API & Native Insights Connection: Integrating official platform reporting feeds\n"
            "2. Baseline Metrics Compilation: Measuring historical 90-day engagement and follower trends\n"
            "3. Top Content Breakdown: Categorizing top 10% and bottom 10% posts to find success patterns\n"
            "4. Audience Quality Analysis: Evaluating follower growth velocity and location authenticity\n"
            "5. Conversion Tracking Synthesis: Connecting social clicks to website leads and booked calls\n"
            "6. Executive Presentation: Delivering a monthly strategic scorecard with growth recommendations"
        ),
        "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "SEO Reporting",
        "icon_name": "manage_search",
        "short_description": "Monthly executive SEO scorecards tracking keyword ranking shifts, backlink health, organic traffic growth, and competitor movements.",
        "overview": (
            "Track the measurable ROI of your search engine optimization efforts. We provide transparent monthly SEO reporting "
            "highlighting keyword position shifts on Google, organic traffic growth, new authoritative backlinks earned, "
            "high-converting search landing pages, and competitive rank changes across your local and national target market."
        ),
        "benefits": (
            "Accurate Google Keyword Position Tracking across desktop and mobile search\n"
            "Organic Traffic Revenue Attribution showing which organic keywords lead to inquiries\n"
            "Backlink Health & Toxicity Monitoring protecting your site from spammy backlink attacks\n"
            "Competitor Ranking Movements showing where you are gaining or losing market share\n"
            "Local Map Pack Visibility Scorecards tracking Google Maps local 3-pack dominance\n"
            "Jargon-Free Executive Summaries written in plain business English for decision-makers"
        ),
        "process": (
            "1. Keyword Tracking Setup: Tracking high-intent commercial keyword rankings across target cities\n"
            "2. Backlink Profile Auditing: Measuring domain authority, new referring domains, and anchor text\n"
            "3. Traffic & Conversions Attribution: Correlating Google organic sessions with leads generated\n"
            "4. Technical Health Re-Checks: Scanning for broken links, duplicate titles, and crawl errors\n"
            "5. Monthly Scorecard Production: Generating clean, visual PDF reports with historical charts\n"
            "6. Strategy Alignment Call: Reviewing progress and identifying next month's target keywords"
        ),
        "image_url": "https://images.unsplash.com/photo-1572021335469-31706a17aaef?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Sales Dashboards",
        "icon_name": "point_of_sale",
        "short_description": "Real-time sales performance trackers displaying pipeline value, conversion velocity, monthly recurring revenue, and team quotas.",
        "overview": (
            "Give your sales leaders complete clarity over your revenue engine. We build real-time visual sales dashboards "
            "that connect directly to your CRM, e-commerce store, or POS system. Display metrics like total pipeline value, "
            "average deal size, sales rep quota attainment, lead-to-close conversion velocity, and Monthly Recurring Revenue (MRR)."
        ),
        "benefits": (
            "Live Real-Time Revenue Tracking showing closed deals and cash collected by the minute\n"
            "Pipeline Stage Visibility: Identify exactly where deals stall or drop off in your funnel\n"
            "Individual Sales Rep Leaderboards tracking calls made, meetings booked, and revenue closed\n"
            "Accurate Sales Forecasting Models predicting month-end and quarter-end revenue\n"
            "Average Sales Cycle Velocity: Measure how many days it takes a lead to become a paid customer\n"
            "Mobile-Friendly Cloud Access allowing executives to view sales metrics from anywhere"
        ),
        "process": (
            "1. Sales Process & Pipeline Mapping: Defining deal stages, qualification rules, and win criteria\n"
            "2. Data Source Connection: Integrating CRM (HubSpot, Zoho, Salesforce), Stripe, or M-Pesa\n"
            "3. Metric KPI Calculation: Formulating MRR, win rate %, average deal size, and pipeline health\n"
            "4. Dashboard UI Wireframing: Designing high-contrast visual charts, gauges, and leaderboards\n"
            "5. Automated Refresh Scheduling: Configuring live webhooks or 15-minute sync intervals\n"
            "6. User Permissions & Rollout: Setting up role-based access for management and sales reps"
        ),
        "image_url": "https://images.unsplash.com/photo-1543286386-713bdd548da4?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Business Dashboards",
        "icon_name": "dashboard",
        "short_description": "Centralized executive operational dashboards unifying revenue, expenses, inventory velocity, and customer lifetime value.",
        "overview": (
            "Run your company on real-time facts, not gut feelings. We build centralized Executive Business Dashboards "
            "that aggregate data across all company departments—Finance, Marketing, Sales, Operations, and Customer Support. "
            "Get a single-screen command center showing net profit margins, cash flow, customer acquisition costs, and operational bottlenecks."
        ),
        "benefits": (
            "Single-Screen Company Command Center unifying cross-departmental operations\n"
            "Real-Time Net Profit & Cash Flow Tracking consolidating revenue against operating expenses\n"
            "Customer Lifetime Value (LTV) to Customer Acquisition Cost (CAC) Ratio Monitoring\n"
            "Inventory Turnover & Stock Alerts preventing stockouts and overstocked cash traps\n"
            "Support Ticket Resolution Velocity tracking customer satisfaction and response speed\n"
            "Automated Slack / Email Alert Triggers when key business metrics dip below thresholds"
        ),
        "process": (
            "1. Executive Stakeholder Workshop: Identifying the top 5 vital North Star business metrics\n"
            "2. Data Source Architecture: Connecting accounting software, CRM, marketing ads, and inventory\n"
            "3. Data Cleaning & Transformation: Normalizing disparate datasets into a unified warehouse\n"
            "4. Executive Dashboard Design: Crafting intuitive, clean visual cards and trend graphs\n"
            "5. Threshold Alert Configuration: Setting automatic notifications for revenue spikes or drops\n"
            "6. Management Training: Training executive leadership on dashboard drill-down capabilities"
        ),
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Excel Data Analysis",
        "icon_name": "table_view",
        "short_description": "Advanced Excel models with automated macro scripts, pivot tables, financial forecasting models, and interactive dashboard templates.",
        "overview": (
            "Unlock the full power of Microsoft Excel to automate business reporting and financial modeling. "
            "We build sophisticated Excel workbooks featuring automated Power Query data cleaning, dynamic Pivot Tables, "
            "financial forecasting models, interactive slicer dashboards, and VBA macros that turn hours of manual spreadsheet work into a 1-click task."
        ),
        "benefits": (
            "Automated Data Cleaning via Power Query: Ingest raw CSVs and clean them with 1 click\n"
            "Interactive Slicer Dashboards allowing non-technical managers to filter data dynamically\n"
            "Financial Modeling & Sensitivity Analysis projecting cash flow, break-even, and profit\n"
            "VBA Macro Automation eliminating repetitive daily and weekly spreadsheet tasks\n"
            "Error-Proof Data Validation formulas preventing accidental data corruption\n"
            "Professional Executive Formatting ready for board presentations and investor pitches"
        ),
        "process": (
            "1. Data Structure Audit: Reviewing your existing messy spreadsheets and manual processes\n"
            "2. Power Query Pipeline Construction: Automating data extraction, formatting, and filtering\n"
            "3. Formula Engineering: Implementing dynamic INDEX-MATCH, XLOOKUP, and conditional logic\n"
            "4. Interactive Dashboard Layer: Building Pivot Charts, timeline slicers, and summary cards\n"
            "5. Macro Automation & Testing: Writing VBA scripts for automated export and report delivery\n"
            "6. Documentation & Handover: Providing a user guide so anyone on your team can operate it"
        ),
        "image_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Power BI Dashboards",
        "icon_name": "insert_chart",
        "short_description": "Enterprise Microsoft Power BI data pipelines with interactive drill-down reports, scheduled refreshes, and cloud sharing.",
        "overview": (
            "Transform massive corporate datasets into interactive visual stories. We develop enterprise Microsoft Power BI dashboards "
            "with custom DAX measures, automated cloud data refreshes, drill-through capabilities, and role-level security (RLS). "
            "Empower department managers to slice and dice years of sales, logistics, and operational data with fluid interactivity."
        ),
        "benefits": (
            "Interactive Drill-Down Capabilities: Click any country or product to filter the entire report\n"
            "Automated Cloud Gateway Refreshes ensuring data is always updated without manual work\n"
            "Complex DAX Modeling calculating Year-over-Year (YoY) growth, running totals, and margins\n"
            "Role-Level Security (RLS): Ensure branch managers only see data from their own branch\n"
            "Mobile App Compatibility enabling leadership to view reports on iPad, iPhone, and Android\n"
            "Embedded Power BI Reports integrated directly into your private company portal or website"
        ),
        "process": (
            "1. Data Architecture & Source Connection: Connecting SQL databases, Excel, and cloud APIs\n"
            "2. Star Schema Data Modeling: Designing clean relationships between Fact and Dimension tables\n"
            "3. Advanced DAX Formula Construction: Formulating custom business intelligence calculations\n"
            "4. Visual UI/UX Layout Design: Applying corporate colors, interactive bookmarks, and tooltips\n"
            "5. Power BI Service Publishing: Setting up cloud workspaces, security roles, and refresh schedules\n"
            "6. User Training & Documentation: Conducting walkthrough sessions for business analysts"
        ),
        "image_url": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Python Data Analysis",
        "icon_name": "terminal",
        "short_description": "Custom Python data pipelines using Pandas, NumPy, and Scikit-Learn for customer segmentation, predictive modeling, and automated ETL.",
        "overview": (
            "Harness advanced data science and machine learning for your business. We develop automated Python data pipelines "
            "using Pandas, NumPy, Scikit-Learn, and Matplotlib. Deliverables include automated web scraping, API data extraction, "
            "unsupervised customer clustering, sales demand forecasting, and automated PDF report compilation."
        ),
        "benefits": (
            "Handling Massive Datasets with millions of rows that crash traditional spreadsheet tools\n"
            "Automated ETL Pipelines: Extract data from APIs, transform, and load into databases seamlessly\n"
            "Machine Learning Customer Clustering (K-Means) segmenting buyers by profitability\n"
            "Predictive Sales Forecasting using statistical time-series models (ARIMA / Prophet)\n"
            "Custom Automated Data Scraping gathering competitor pricing and market trends\n"
            "Well-Documented Clean Code provided in Jupyter Notebooks or containerized Docker scripts"
        ),
        "process": (
            "1. Problem Definition & Dataset Collection: Ingesting raw database dumps, APIs, and flat files\n"
            "2. Exploratory Data Analysis (EDA): Cleaning anomalies, imputing missing values, and plotting trends\n"
            "3. Feature Engineering: Creating behavioral metrics and normalizing input parameters\n"
            "4. Model Development & Validation: Training machine learning models with cross-validation\n"
            "5. Pipeline Automation: Scripting automated daily execution with logging and error handling\n"
            "6. Delivery & Knowledge Transfer: Delivering source code, notebooks, and executive slide deck"
        ),
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Customer Data Analysis",
        "icon_name": "groups",
        "short_description": "Churn prediction analysis, customer cohort behavior modeling, Net Promoter Score evaluation, and repeat purchase drivers.",
        "overview": (
            "Discover who your most profitable customers are and keep them for life. We analyze your historical customer data "
            "to build RFM (Recency, Frequency, Monetary) segmentation models, calculate Customer Lifetime Value (CLV), "
            "detect early churn warning signals before clients leave, and identify the exact triggers that produce repeat purchases."
        ),
        "benefits": (
            "RFM Segmentation: Pinpoint your VIP Champions, Loyalists, and At-Risk customer cohorts\n"
            "Accurate Customer Lifetime Value (CLV) Calculation determining safe acquisition budgets\n"
            "Early Churn Detection Models alerting your account managers before high-value clients leave\n"
            "Repeat Purchase Timing Analysis finding the exact day to send re-order reminder offers\n"
            "Net Promoter Score (NPS) & Sentiment Correlation linking review feedback to retention\n"
            "Actionable Retention Playbook outlining targeted email and WhatsApp campaigns for each cohort"
        ),
        "process": (
            "1. Transactional History Ingestion: Pulling customer purchase logs from CRM and e-commerce\n"
            "2. RFM Metric Scoring: Scoring recency, purchase frequency, and lifetime spend per customer\n"
            "3. Cohort Retention Curves: Graphing monthly retention decay curves and drop-off milestones\n"
            "4. Churn Risk Modeling: Identifying behavior signals (inactivity, drop in tickets) preceding churn\n"
            "5. Actionable Segmentation Output: Generating tagged contact lists ready for marketing automation\n"
            "6. Retention Strategy Presentation: Guiding leadership on loyalty incentives and win-back drips"
        ),
        "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80"
    },
    {
        "category_slug": "analytics-business-intelligence",
        "title": "Marketing Performance Analysis",
        "icon_name": "pie_chart",
        "short_description": "Full-funnel attribution modeling tracking customer acquisition cost (CAC), return on ad spend (ROAS), and multi-touch conversions.",
        "overview": (
            "Stop wasting marketing budget on underperforming channels. We perform rigorous full-funnel marketing analytics "
            "connecting ad spend across Meta, Google Ads, TikTok, and SEO directly to bottom-line revenue. "
            "Our multi-touch attribution models uncover which marketing touchpoints genuinely initiate, nurture, and close paying clients."
        ),
        "benefits": (
            "Accurate True Return on Ad Spend (ROAS) accounting for offline sales and WhatsApp closes\n"
            "True Blended Customer Acquisition Cost (CAC) across all digital and offline channels\n"
            "Multi-Touch Attribution Modeling: First-click, Linear, and Last-touch conversion comparison\n"
            "Campaign Budget Reallocation: Shift ad spend from unprofitable campaigns to winners\n"
            "Customer Journey Dwell Time: Measure how many touchpoints and days a lead requires before buying\n"
            "Executive Marketing Scorecard clearly proving marketing's direct contribution to company revenue"
        ),
        "process": (
            "1. Full-Funnel Tracking Audit: Ensuring UTM parameters, conversion APIs, and CRM tags match\n"
            "2. Spend & Revenue Consolidation: Combining advertising ad spend receipts with realized sales\n"
            "3. Multi-Touch Attribution Modeling: Analyzing initial discovery touchpoints vs. closing channels\n"
            "4. Channel Profitability Breakdown: Calculating net profit margin generated by each ad channel\n"
            "5. Waste Identification: Pinpointing keywords, ad placements, and demographics draining budget\n"
            "6. Strategic Budget Reallocation Plan: Providing executive recommendations for next quarter's budget"
        ),
        "image_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80"
    }
]
