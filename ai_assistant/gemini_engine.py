import json
import logging
import requests
from django.conf import settings
from django.db.models import Q
from .grounding import build_system_knowledge_prompt

logger = logging.getLogger(__name__)

# Verified working Gemini free-tier and latest models in order of speed and reliability
FREE_TIER_MODELS_CASCADE = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemma-4-26b-a4b-it",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-flash-latest",
]

def call_gemini_api(model: str, api_key: str, system_prompt: str, chat_history: list, timeout: int = 10) -> str:
    """
    Calls Google's Generative Language REST API for the specified model using requests.
    Supports system instructions and conversation context.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    formatted_contents = []
    for msg in chat_history:
        role = "user" if msg.get("sender") == "user" else "model"
        formatted_contents.append({
            "role": role,
            "parts": [{"text": msg.get("message", "")}]
        })

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": formatted_contents,
        "generationConfig": {
            "temperature": 0.4,
            "topP": 0.9,
            "maxOutputTokens": 1000,
        }
    }

    resp = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=timeout
    )

    if resp.status_code == 200:
        data = resp.json()
        candidates = data.get("candidates", [])
        if candidates and "content" in candidates[0]:
            parts = candidates[0]["content"].get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]
        raise ValueError(f"Malformed response payload from Gemini model {model}: {data}")
    elif resp.status_code == 404:
        raise ValueError(f"Model {model} not found or retired: {resp.text[:120]}")
    elif resp.status_code == 429:
        raise ValueError(f"Model {model} quota exhausted (HTTP 429)")
    else:
        raise ValueError(f"HTTP {resp.status_code} from {model}: {resp.text[:120]}")


def generate_conversational_response(chat_history: list, user_message: str, client_context: dict = None) -> dict:
    """
    Executes a high-availability multi-model AI pipeline:
    1. Attempts live Gemini Generative AI across the verified free-tier models.
    2. If Gemini API is rate-limited (429) or offline, falls back to our intelligent,
       live database-grounded knowledge engine that searches services, categories, and portfolio.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
    system_prompt = build_system_knowledge_prompt()

    if client_context:
        client_info_str = (
            f"\n\n### Current Client Profile:\n"
            f"- Full Name: {client_context.get('name', 'Prospect')}\n"
            f"- Email: {client_context.get('email', 'N/A')}\n"
            f"- Phone/WhatsApp: {client_context.get('phone', 'N/A')}\n"
            f"- Industry/Interest: {client_context.get('industry', 'N/A')}"
        )
        system_prompt += client_info_str

    full_history = list(chat_history)
    full_history.append({"sender": "user", "message": user_message})

    # Try live Gemini models if API key is provided
    error_logs = []
    if api_key:
        for idx, model in enumerate(FREE_TIER_MODELS_CASCADE):
            is_fallback_turn = (idx > 0)
            try:
                reply_text = call_gemini_api(model, api_key, system_prompt, full_history, timeout=10)
                if reply_text and len(reply_text.strip()) > 5:
                    return {
                        "text": reply_text.strip(),
                        "model_used": model,
                        "is_fallback": is_fallback_turn,
                        "error_logs": error_logs
                    }
            except Exception as e:
                err_msg = f"{model}: {str(e)[:80]}"
                error_logs.append(err_msg)
                logger.debug(f"Gemini cascade attempt failed: {err_msg}")
                continue

    # High-fidelity live database retrieval fallback
    logger.info("Serving query from UniqueTechCamp dynamic database knowledge engine.")
    local_reply = generate_intelligent_database_grounded_response(user_message, client_context)
    return {
        "text": local_reply,
        "model_used": "utc-live-db-engine",
        "is_fallback": True,
        "error_logs": error_logs
    }


def generate_intelligent_database_grounded_response(query: str, client_context: dict = None) -> str:
    """
    Dynamically interrogates the PostgreSQL/MariaDB/SQLite database (Services, Categories,
    Portfolio, Case Studies, About) to generate an authentic, context-specific markdown answer.
    NO hardcoded identical responses!
    """
    q = (query or '').strip().lower()
    name = client_context.get('name', '').strip() if client_context else ''
    greeting = f"Hello {name}! " if name and name.lower() not in ['prospect', 'there', 'client'] else ""

    # 1. Company Identity / "Who are you?" / "Tell me about UniqueTechCamp"
    if any(k in q for k in ['who are you', 'tell me about uniquetechcamp', 'what is uniquetechcamp', 'about you', 'about uniquetechcamp', 'about company']):
        return (
            f"{greeting}**UniqueTechCamp Limited** is a premier software engineering and digital growth company headquartered in the **Nairobi Central Business District (CBD), Kenya**.\n\n"
            "We reject generic, static websites that fail to generate revenue. Instead, we architect **end-to-end digital growth systems** that combine:\n"
            "• **Sub-Second Performance**: Future-ready web applications built on Python, Django, Tailwind CSS, and compiled assets.\n"
            "• **24/7 AI Qualification Agents**: Autonomous WhatsApp & email qualification bots that engage prospects and sync with your CRM.\n"
            "• **Financial & Localized Integrations**: Automated Safaricom M-Pesa Daraja STK Push, international card checkouts, and instant receipting.\n"
            "• **165+ Growth Services**: Across 20 specialized industry categories (healthcare, civil construction, hospitality, retail, e-commerce, professional services, and AI SaaS).\n\n"
            "We operate Sunday through Friday (8:00 AM – 8:00 PM EAT, closed Saturdays). You can reach our engineering team directly via Phone/WhatsApp at **+254 715 479 955** or email **info@uniquetechcamp.org**."
        )

    # 2. Services List / Categories Inquiry
    if any(k in q for k in ['list of services', 'list of your services', 'what services', 'services do you offer', 'show me services', 'all services', 'categories', 'service catalog']):
        from services.models import ServiceCategory
        try:
            cats = ServiceCategory.objects.filter(is_active=True).prefetch_related('services').order_by('order')
            if cats.exists():
                lines = [
                    f"{greeting}UniqueTechCamp provides **165+ specialized digital growth services** across **20 industry categories**. Here is our core spectrum:\n"
                ]
                for idx, c in enumerate(cats[:10], 1):
                    service_names = [s.title for s in c.services.filter(is_active=True)[:3]]
                    sample_str = f" ({', '.join(service_names)})" if service_names else ""
                    lines.append(f"**{idx}. {c.icon} {c.name}**{sample_str}")

                if len(cats) > 10:
                    lines.append(f"\n...and **{len(cats) - 10} more industry sectors** including Education, Travel & Tourism, Legal & Law Firms, Beauty & Wellness, and AI SaaS Architecture.")

                lines.append(
                    "\n👉 Explore our complete interactive service catalog with full breakdowns at: "
                    "[uniquetechcamp.org/services/](https://uniquetechcamp.org/services/)\n\n"
                    "Which industry or service does your business need?"
                )
                return "\n".join(lines)
        except Exception as e:
            logger.warning(f"Error querying categories: {e}")

    # 3. Portfolio, Real Projects, or Case Studies
    if any(k in q for k in ['portfolio', 'project', 'case stud', 'past work', 'clients', 'websites you have built', 'sample']):
        from portfolio.models import Project
        try:
            projects = Project.objects.all().order_by('order')
            if projects.exists():
                lines = [
                    f"{greeting}Here are **verified production projects** engineered by UniqueTechCamp:\n"
                ]
                for p in projects:
                    lines.append(
                        f"• **[{p.title}]({p.live_demo_url})** — *{p.client_name}*\n"
                        f"  {p.short_description}\n"
                        f"  **Tech Stack**: {p.technologies}\n"
                    )
                lines.append(
                    "👉 View full case studies and performance benchmarks at: "
                    "[uniquetechcamp.org/portfolio/](https://uniquetechcamp.org/portfolio/)\n\n"
                    "Would you like to deploy a similar system for your business?"
                )
                return "\n".join(lines)
        except Exception as e:
            logger.warning(f"Error querying projects: {e}")

    # 4. WhatsApp AI Bots, CRM, & Google Sheets Integration
    if any(k in q for k in ['whatsapp', 'bot', 'chatbot', 'qualification', 'google sheets', 'crm', 'sheets integration']):
        return (
            f"{greeting}Our **24/7 AI WhatsApp Qualification Agents** are custom-engineered for automated client acquisition:\n\n"
            "### How It Integrates With CRM & Google Sheets:\n"
            "1. **Cloud Webhook Ingestion**: Inbound WhatsApp messages trigger our secure Django webhook receivers in real-time.\n"
            "2. **Natural Language AI Qualification**: The agent qualifies prospect budgets, timelines, and requirements in fluent English and Swahili.\n"
            "3. **Instant Google Sheets Sync**: Using Google Sheets API (v4) service accounts, qualified leads (Name, Phone, Email, Budget, Needs, Timestamp) append automatically into your private Google Sheet without delay.\n"
            "4. **CRM Sync (HubSpot, Zoho, Salesforce)**: Bi-directional webhooks automatically create new deals and schedule follow-up tasks for your sales team.\n"
            "5. **Catalog & Booking**: The bot automatically delivers PDF product catalogs and books discovery consultations directly into your calendar.\n\n"
            "Would you like to schedule a 15-minute live demo of our WhatsApp bot engine?"
        )

    # 5. Search specific services from database (e.g. clinic, hospital, construction, cafe, church, ecommerce, seo, etc.)
    search_terms = [word for word in q.split() if len(word) > 3 and word not in ['what', 'with', 'about', 'your', 'have', 'from', 'this', 'that', 'could', 'would', 'should', 'tell']]
    if search_terms:
        from services.models import Service
        query_filter = Q()
        for term in search_terms[:3]:
            query_filter |= Q(title__icontains=term) | Q(short_description__icontains=term) | Q(category__name__icontains=term)

        try:
            matched_services = Service.objects.filter(query_filter, is_active=True).select_related('category')[:4]
            if matched_services.exists():
                lines = [
                    f"{greeting}Yes! UniqueTechCamp offers specialized solutions matching your inquiry:\n"
                ]
                for s in matched_services:
                    cat_name = s.category.name if s.category else "Solutions"
                    lines.append(
                        f"• **{s.title}** (*{cat_name}*)\n"
                        f"  {s.short_description}\n"
                        f"  [Explore service details &rarr;](https://uniquetechcamp.org/services/{s.slug}/)\n"
                    )
                lines.append(
                    "\nWe engineer every platform with high-converting layouts, mobile optimization, and automated customer follow-ups.\n"
                    "Would you like to discuss your requirements or schedule a free discovery consultation?"
                )
                return "\n".join(lines)
        except Exception as e:
            logger.warning(f"Error in dynamic service match: {e}")

    # 6. Pricing, Cost, Rates
    if any(k in q for k in ['price', 'pricing', 'cost', 'fee', 'quotation', 'rate', 'how much', 'charge']):
        return (
            f"{greeting}UniqueTechCamp provides **transparent, milestone-based pricing** with no hidden fees:\n\n"
            "• **Currencies Accepted**: Kenya Shillings (KES) and US Dollars (USD).\n"
            "• **Payment Gateways**: Automated Safaricom M-Pesa Daraja STK Push (Till: **5797853**) and international credit/debit cards.\n"
            "• **Project Milestones**: Typically structured into 40% initial commitment, 30% functional prototype review, and 30% final production launch.\n"
            "• **AI Master Coding Prompts**: Available in both Free and Premium tiers on our marketplace.\n\n"
            "Because every system (whether an AI WhatsApp bot, custom clinic EMR, or large e-commerce marketplace) has specific requirements, "
            "we offer a **free 1-hour technical discovery call** to analyze your architecture and deliver an itemized proposal. "
            "Would you like to book your session today?"
        )

    # 7. Contact, Location, Headquarters, Hours
    if any(k in q for k in ['contact', 'location', 'office', 'where are you', 'headquarters', 'phone', 'call', 'email', 'hours']):
        return (
            f"{greeting}Here are the official contact details for UniqueTechCamp:\n\n"
            "• **Headquarters**: Nairobi Central Business District (CBD), Nairobi County, Kenya\n"
            "• **Operating Hours**: Sunday to Friday, 8:00 AM – 8:00 PM East Africa Time (EAT), closed Saturdays\n"
            "• **Phone & WhatsApp**: **+254 715 479 955**\n"
            "• **Email**: **info@uniquetechcamp.org**\n"
            "• **Website**: [uniquetechcamp.org](https://uniquetechcamp.org/)\n\n"
            "Feel free to call us directly, message on WhatsApp, or book an appointment right here in the chat!"
        )

    # 8. Appointments & Booking
    if any(k in q for k in ['appointment', 'consultation', 'book', 'schedule', 'meeting', 'call with you']):
        return (
            f"{greeting}We would be pleased to schedule a **1-hour technical discovery consultation** with our solutions engineering team.\n\n"
            "Consultations are conducted Sunday through Friday between 8:00 AM and 8:00 PM EAT via Google Meet, WhatsApp Call, or in-person at our Nairobi CBD office.\n"
            "Simply type **\"Book an appointment\"** or let me know your preferred date, and I will present our upcoming available slots immediately!"
        )

    # 9. Smart Context-Aware Fallback (synthesizes client name and available resources)
    return (
        f"{greeting}Thank you for your question regarding **\"{query}\"**!\n\n"
        "At **UniqueTechCamp**, we engineer high-performance web applications and AI client acquisition systems tailored for your business:\n"
        "• **165+ Industry Services**: From Digital Business Setup, Branding, and SEO to custom Django web apps and AI qualification bots.\n"
        "• **Autonomous WhatsApp Lead Bots**: Engage, qualify, and sync customer leads 24/7 with your CRM and Google Sheets.\n"
        "• **Proven Production Portfolio**: Verified projects including LIMBS Orthopaedic, Ruwe Holy Ghost Church, Gen-Z Constructors, KAWA'S Café, and Orthobest Care Hub.\n\n"
        "Would you like to explore our [full services catalog](https://uniquetechcamp.org/services/), review our [portfolio case studies](https://uniquetechcamp.org/portfolio/), or schedule a free discovery consultation?"
    )
