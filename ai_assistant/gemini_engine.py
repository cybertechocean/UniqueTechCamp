import json
import logging
import urllib.request
import urllib.error
from django.conf import settings
from .grounding import build_system_knowledge_prompt

logger = logging.getLogger(__name__)

# Free tier cascading models list
FREE_TIER_MODELS_CASCADE = [
    "gemini-3.6-flash",
    "gemini-2.5-flash-lite",
    "gemma-4-26b-a4b-it",
    "gemini-flash-latest",
]

POLISHED_PEAK_FALLBACK_MESSAGE = (
    "Our technical advisory desk is currently handling peak inquiries. "
    "Your message and contact details have been safely recorded, and our engineering team will follow up directly "
    "via WhatsApp or email shortly. You can also reach our live desk immediately at +254 715 479 955."
)

def call_gemini_api(model: str, api_key: str, system_prompt: str, chat_history: list, timeout: int = 6):
    """
    Calls Google's Generative Language REST API for the specified model.
    Accepts system instruction and conversation history.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    # Format contents for Gemini API
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
            "maxOutputTokens": 800,
        }
    }

    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=timeout) as response:
        res_body = response.read().decode('utf-8')
        data = json.loads(res_body)
        candidates = data.get("candidates", [])
        if candidates and "content" in candidates[0]:
            parts = candidates[0]["content"].get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]
        raise ValueError(f"Malformed response payload from Gemini model {model}: {data}")


def generate_conversational_response(chat_history: list, user_message: str, client_context: dict = None):
    """
    Executes a multi-model cascading fallback pipeline across free-tier Gemini variants.
    Intercepts HTTP 429 quota exhaustion and timeouts silently.
    Returns a dict:
      {
        "text": str,
        "model_used": str,
        "is_fallback": bool,
        "error_logs": list
      }
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
    system_prompt = build_system_knowledge_prompt()

    # Append client profile context if known
    if client_context:
        client_info_str = f"\nClient Profile Known:\n- Name: {client_context.get('name', 'Prospect')}\n- Email: {client_context.get('email', 'N/A')}\n- Phone: {client_context.get('phone', 'N/A')}"
        system_prompt += client_info_str

    full_history = list(chat_history)
    full_history.append({"sender": "user", "message": user_message})

    # If no API key configured, use our intelligent local grounded knowledge engine
    if not api_key:
        logger.info("No GEMINI_API_KEY found. Utilizing high-fidelity local grounded knowledge engine.")
        mock_response = generate_local_grounded_response(user_message, client_context)
        return {
            "text": mock_response,
            "model_used": "utc-grounded-knowledge-v1",
            "is_fallback": False,
            "error_logs": ["Simulated local grounded mode (no GEMINI_API_KEY configured)"]
        }

    error_logs = []
    for idx, model in enumerate(FREE_TIER_MODELS_CASCADE):
        is_fallback_turn = (idx > 0)
        try:
            logger.info(f"Dispatching query to Gemini model: {model} (Fallback Level: {idx})")
            reply_text = call_gemini_api(model, api_key, system_prompt, full_history)
            return {
                "text": reply_text.strip(),
                "model_used": model,
                "is_fallback": is_fallback_turn,
                "error_logs": error_logs
            }
        except urllib.error.HTTPError as he:
            err_msg = f"HTTPError {he.code} on model {model}: {he.reason}"
            logger.warning(err_msg)
            error_logs.append(err_msg)
            # If 429 or 503, continue cascade silently
            continue
        except Exception as e:
            err_msg = f"Exception on model {model}: {str(e)}"
            logger.warning(err_msg)
            error_logs.append(err_msg)
            continue

    # If all remote models in the cascade failed or timed out, serve intelligent domain-grounded response
    logger.info("Serving domain-grounded response from UniqueTechCamp knowledge engine.")
    local_reply = generate_local_grounded_response(user_message, client_context)
    return {
        "text": local_reply,
        "model_used": "utc-knowledge-engine",
        "is_fallback": True,
        "error_logs": error_logs
    }


def generate_local_grounded_response(query: str, client_context: dict = None) -> str:
    """
    High-fidelity deterministic local fallback responder when offline or without Gemini API key.
    Provides strictly grounded, brand-accurate responses for UniqueTechCamp services.
    """
    q = query.lower()
    name = client_context.get('name', 'there') if client_context else 'there'

    if any(k in q for k in ['appointment', 'consultation', 'book', 'schedule', 'meeting', 'call']):
        return (
            f"Hello {name}! We'd be delighted to discuss your technical architecture. "
            "UniqueTechCamp offers free 1-hour discovery consultations with our senior engineering team. "
            "You can choose an upcoming slot between Sunday and Friday (8:00 AM – 8:00 PM EAT, Saturdays closed) via Google Meet, "
            "WhatsApp Video, or in-person at our Nairobi CBD office. Would you like to select a preferred date and time?"
        )
    elif any(k in q for k in ['whatsapp', 'bot', 'chatbot', 'automation', 'lead gen']):
        return (
            "At UniqueTechCamp, our 24/7 AI WhatsApp Qualification Agents are engineered to turn conversations into booked sales. "
            "They automatically qualify prospective leads, answer customer FAQs in English and Swahili, send PDF catalogs, "
            "and sync leads directly with your CRM or Google Sheets. Would you like to book a quick consultation or see our live demo?"
        )
    elif any(k in q for k in ['clinic', 'hospital', 'medical', 'patient', 'health']):
        return (
            "Our Healthcare & Clinic Management Systems are customized for private practices, diagnostic clinics, and hospitals. "
            "Key features include online patient appointment booking, doctor queue management, electronic medical records (EMR), "
            "and M-Pesa automated billing integration. We can customize the platform to your workflow within 2 to 3 weeks."
        )
    elif any(k in q for k in ['ecommerce', 'e-commerce', 'shop', 'store', 'm-pesa', 'daraja', 'payment']):
        return (
            "We engineer high-converting digital storefronts and e-commerce portals with instant M-Pesa Daraja STK Push "
            "and international card checkouts. Our platforms feature sub-second load times, inventory tracking, and client self-service "
            "order tracking. Would you like to schedule a strategy call to scope your product catalog?"
        )
    elif any(k in q for k in ['price', 'pricing', 'cost', 'fee', 'rate', 'how much']):
        return (
            "Our project investment depends on your specific scope and integrations: for example, custom WhatsApp AI bots, "
            "bespoke web applications, or enterprise SaaS engines each have tailored milestones. "
            "We provide transparent milestone-based pricing in KES or USD. Schedule a free technical discovery call with us "
            "so we can evaluate your requirements and provide an itemized architecture proposal."
        )
    elif any(k in q for k in ['contact', 'location', 'where', 'phone', 'email', 'address']):
        return (
            "UniqueTechCamp is headquartered in the Nairobi Central Business District (CBD), Nairobi County, Kenya. "
            "Our support and engineering desk operates Sunday to Friday from 8:00 AM to 8:00 PM East Africa Time (EAT), closed on Saturdays. "
            "You can reach us directly via Phone/WhatsApp at **+254 715 479 955** or email us at **info@uniquetechcamp.org**."
        )
    else:
        return (
            f"Thank you for contacting UniqueTechCamp, {name}! We engineer end-to-end digital growth systems—including "
            "high-converting web applications, 24/7 AI WhatsApp qualification agents, clinic systems, and e-commerce platforms. "
            "How can our solutions architecture team assist your business today?"
        )
