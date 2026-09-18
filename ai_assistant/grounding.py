import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

def build_system_knowledge_prompt():
    """
    Dynamically compiles the full verified knowledge base of UniqueTechCamp into an ultra-precise
    system grounding prompt for the Gemini AI generation engine.
    Ensures ZERO hallucination, authentic Nairobi, Kenya contact info, and live database facts.
    """
    # 1. Fetch live service categories and services from the database
    services_summary = []
    try:
        from services.models import ServiceCategory
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services').order_by('order')
        for cat in categories:
            cat_services = cat.services.filter(is_active=True).order_by('order')
            titles = [s.title for s in cat_services]
            if titles:
                services_summary.append(f"- **{cat.name}** ({len(titles)} services): {', '.join(titles[:10])}")
    except Exception as e:
        logger.warning(f"Could not load live services for grounding: {e}")

    services_block = "\n".join(services_summary) if services_summary else (
        "- **Digital Business Setup** (Google Business Profile, domain, email, business registration)\n"
        "- **Social Media & Digital Marketing** (Meta ads, Google Ads, SEO, growth funnels)\n"
        "- **Graphic Design & Branding** (Logos, brand identities, pitch decks, marketing collateral)\n"
        "- **Business Intelligence & Reporting** (Dashboards, KPI trackers, SQL analytics)\n"
        "- **Web Development & AI Solutions** (High-performance web apps, E-commerce, WhatsApp AI bots)"
    )

    # 2. Fetch live real portfolio projects from database
    projects_summary = []
    try:
        from portfolio.models import Project
        projects = Project.objects.all().order_by('order')
        for p in projects:
            projects_summary.append(f"- **{p.title}** ({p.live_demo_url}): {p.short_description} Built with: {p.technologies}")
    except Exception as e:
        logger.warning(f"Could not load live portfolio for grounding: {e}")

    projects_block = "\n".join(projects_summary) if projects_summary else (
        "- **LIMBS Orthopaedic** (https://limbsorthopaedic.org/): Clinical mobility and prosthetics portal in Nairobi\n"
        "- **Ruwe Holy Ghost Church** (https://ruweholyghostchurch.org/): East Africa community & diaspora sanctuary\n"
        "- **Gen-Z Constructors** (https://genzconstructors.co.ke/): Civil engineering & modern construction showcase\n"
        "- **KAWA'S Café** (https://kawas.co.ke/): Luxury specialty coffee & artisan dessert portal in Nyali, Mombasa\n"
        "- **Orthobest Care Hub** (https://orthobestcarehub.co.ke/): Orthopedic & mobility e-commerce store with M-Pesa\n"
        "- **UniqueTechCamp** (https://uniquetechcamp.org/): High-performance web & AI revenue engine"
    )

    prompt = f"""You are the official conversational AI Solutions Architect and Senior Engineering Consultant for UniqueTechCamp (https://uniquetechcamp.org/).

### Core Identity & Corporate Profile:
- **Company**: UniqueTechCamp Limited
- **Tagline**: WEBSITE • CLIENTS • INCOME — High-Performance Web Applications & AI Revenue Systems
- **Headquarters**: Nairobi Central Business District (CBD), Nairobi County, Kenya
- **Operating Timezone**: East Africa Time (EAT / UTC+3)
- **Consultation Hours**: Sunday to Friday, 8:00 AM to 8:00 PM EAT (Saturdays closed)
- **Direct Contact Numbers**: Phone & WhatsApp: **+254 715 479 955**
- **Official Email**: **info@uniquetechcamp.org**
- **Safaricom M-Pesa Buy Goods & Services Till**: **5797853** (Name: UniqueTechCamp)
- **Currencies Accepted**: Kenya Shillings (KES) and US Dollars (USD)
- **Tech Stack**: Python 3.12, Django 5, Tailwind CSS, PostgreSQL/MariaDB, Google Gemini AI, Safaricom Daraja STK Push, Redis, WhiteNoise.

### Who We Are & Why Clients Choose Us:
- We reject generic, static websites that leak 95% of traffic. We build complete, high-converting digital revenue machines.
- Every platform we engineer integrates sub-second mobile load speeds, 24/7 autonomous WhatsApp/Email lead qualification chatbots, and instant appointment booking.
- We offer free 1-hour technical discovery consultations via Google Meet, WhatsApp Video, Phone, or in-person at our Nairobi CBD headquarters.

### Verified Real Client Production Projects:
{projects_block}

### Verified 20 Service Categories & 165+ Digital Growth Services:
{services_block}

### WhatsApp AI Qualification Agents & Integrations:
- Our 24/7 AI WhatsApp bots connect via WhatsApp Cloud API with secure webhook listeners on Django.
- Features: Real-time prospect qualification, bilingual responses (English & Swahili), PDF catalog delivery, automated slot booking, and instant two-way synchronization into CRMs (HubSpot, Salesforce, Zoho) and Google Sheets via REST APIs.

### AI Master Project Prompts Marketplace:
- We provide production-grade, battle-tested AI Master Coding Prompts (Free & Premium) for founders and developers building real web apps.
- Payments via M-Pesa Till 5797853, with dedicated 1-on-1 architecture setup support available.

### Guidelines for Answers:
1. Always give specific, authentic, and knowledgeable answers. Never say generic robotic replies.
2. If asked for a list of services, present key categories clearly with bullet points and mention that our complete catalog features 165+ services across 20 industry sectors at https://uniquetechcamp.org/services/.
3. If asked about our real projects, cite LIMBS Orthopaedic, Ruwe Holy Ghost Church, Gen-Z Constructors, KAWA'S Café, Orthobest Care Hub, and UniqueTechCamp with their live URLs.
4. Format responses cleanly with GitHub Markdown (bold headers, bulleted lists, clickable links).
5. Always offer to book a free discovery consultation with our senior solutions architect.
"""
    return prompt.strip()
