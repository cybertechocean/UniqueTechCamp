import os
import re
import socket
import logging
from functools import lru_cache
import requests

logger = logging.getLogger(__name__)

# Optional Open-Source Validation Libraries
try:
    import pyisemail
    HAS_PYISEMAIL = True
except ImportError:
    HAS_PYISEMAIL = False

try:
    from validate_email import validate_email as py3_validate_email
    HAS_PY3_VALIDATE_EMAIL = True
except ImportError:
    HAS_PY3_VALIDATE_EMAIL = False

# RFC 5322 Compliant Email Regex Fallback
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)

# Common domain typo corrections for scraped / user-entered emails
DOMAIN_TYPOS = {
    # Google Gmail
    'gamil.com': 'gmail.com',
    'gmaill.com': 'gmail.com',
    'gmial.com': 'gmail.com',
    'gmai.com': 'gmail.com',
    'gmaul.com': 'gmail.com',
    'gamil.co': 'gmail.com',
    'gmail.co': 'gmail.com',
    'gmail.cm': 'gmail.com',
    'gmail.con': 'gmail.com',
    'gmail.coom': 'gmail.com',
    'gmail.cpm': 'gmail.com',
    'gmeil.com': 'gmail.com',
    'gmaill.co': 'gmail.com',
    'googlemail.cm': 'googlemail.com',
    'googlemail.con': 'googlemail.com',
    # Yahoo
    'yaho.com': 'yahoo.com',
    'yahooo.com': 'yahoo.com',
    'yhaoo.com': 'yahoo.com',
    'yahoo.co': 'yahoo.com',
    'yaho.co': 'yahoo.com',
    'yahoo.cm': 'yahoo.com',
    'yahoo.con': 'yahoo.com',
    # Microsoft Hotmail / Outlook
    'hotmial.com': 'hotmail.com',
    'hotmai.com': 'hotmail.com',
    'hotmaill.com': 'hotmail.com',
    'hotmial.co.uk': 'hotmail.co.uk',
    'hotmial.con': 'hotmail.com',
    'outlok.com': 'outlook.com',
    'outloo.com': 'outlook.com',
    'outloock.com': 'outlook.com',
    'outlook.cm': 'outlook.com',
    'outlook.con': 'outlook.com',
    # Apple iCloud
    'iclou.com': 'icloud.com',
    'icoud.com': 'icloud.com',
    'iclould.com': 'icloud.com',
}

# Known temporary / throwaway / disposable email domains
DISPOSABLE_DOMAINS = {
    'mailinator.com', 'tempmail.com', '10minutemail.com', 'guerrillamail.com',
    'throwawaymail.com', 'trashmail.com', 'sharklasers.com', 'yopmail.com',
    'getairmail.com', 'maildrop.cc', 'inboxkitten.com', 'temp-mail.org',
    'fakemailgenerator.com', 'burnermail.io', 'dispostable.com', 'nada.ltd',
    'mohmal.com', 'crazymailing.com', 'tempail.com', 'emailondeck.com',
    'mytemp.email', 'generator.email', 'trashmail.net', 'tempinbox.com',
    'disposablemail.com', 'dropmail.me', 'getnada.com', 'guerrillamail.biz',
    'guerrillamail.de', 'guerrillamail.net', 'guerrillamail.org', 'guerrillamailblock.com',
}

# Dangerous role-based and spam-trap prefixes
DANGEROUS_PREFIXES = {
    'abuse', 'postmaster', 'hostmaster', 'spam', 'spamtrap', 'noc', 'security',
    'mailer-daemon', 'mailerdaemon', 'noreply', 'no-reply', 'donotreply', 'do-not-reply',
}

# Standard role-based prefixes (business general addresses, higher bounce / low open)
ROLE_BASED_PREFIXES = {
    'admin', 'info', 'support', 'contact', 'sales', 'billing', 'help',
    'office', 'service', 'team', 'jobs', 'careers', 'general',
}

# Known hard-bounce SMTP indicators
HARD_BOUNCE_PATTERNS = [
    '550', '5.1.1', '5.1.2', '5.2.1', '5.4.1',
    'does not exist', 'nosuchuser', 'user not found', 'user unknown',
    'mailbox unavailable', 'recipient rejected', 'invalid recipient',
    'no mailbox here', 'undeliverable', 'address rejected', 'account disabled',
    'mailbox not found', 'recipient address rejected',
]

# Invalid scraped TLD typos
INVALID_SCRAPED_TLDS = {
    'con', 'cm', 'cpm', 'cmo', 'og', 'coom', 'ocm', 'comm', 'ney', 'orgg',
    'c0m', 'gmai', 'gamil', 'yaho', 'outlok', 'hotmai', 'hotmial',
}

# Regex to detect scraping text glued to the end of a domain extension
GLUED_SCRAPE_WORDS_REGEX = re.compile(
    r'\.(?:com|org|net|co|ke|co\.ke|io|info)(?:website|phone|call|address|info|contact|office|tel|whatsapp|facebook|instagram|twitter|linkedin|email|site)[a-z0-9]*$',
    re.IGNORECASE
)


def clean_and_normalize_email(raw_email):
    """
    Sanitizes raw email strings scraped from web/Excel:
    - Strips leading/trailing punctuation, quotes, brackets (<, >)
    - Removes internal whitespace
    - Converts to lowercase
    - Corrects known domain typos (e.g. gamil.com -> gmail.com)
    Returns: (cleaned_email, was_typo_fixed)
    """
    if not raw_email:
        return '', False

    cleaned = str(raw_email).strip().lower()
    # Strip angle brackets, quotes, trailing semicolons or commas or dots
    cleaned = cleaned.strip('<>()[]"\'`’‘,;: \t\r\n')
    cleaned = cleaned.rstrip('.')

    # Remove any internal whitespace
    cleaned = re.sub(r'\s+', '', cleaned)

    if '@' not in cleaned:
        return cleaned, False

    parts = cleaned.split('@')
    if len(parts) != 2:
        return cleaned, False

    local_part, domain_part = parts[0], parts[1]

    # Strip trailing punctuation from domain part
    domain_part = domain_part.strip('.,/\\:;')

    # Auto-correct common typos
    was_fixed = False
    if domain_part in DOMAIN_TYPOS:
        domain_part = DOMAIN_TYPOS[domain_part]
        was_fixed = True

    cleaned = f"{local_part}@{domain_part}"
    return cleaned, was_fixed


def detect_scrape_anomaly(email):
    """
    Detects common structural and semantic corruptions from scraped web content:
    - Truncated TLDs or common typo TLDs (.con, .cm, .coom)
    - Concatenated text glued from web scraping (e.g. .comwebsite, .comphone)
    - Double dots or trailing dots
    - Single-character public mailboxes (e.g. a@gmail.com)
    Returns: (is_corrupt, reason)
    """
    if not email or '@' not in email:
        return True, "Missing @ separator"

    local_part, domain = email.split('@', 1)

    # 1. Double dots or dot at start/end
    if '..' in email or local_part.startswith('.') or local_part.endswith('.') or domain.startswith('.') or domain.endswith('.'):
        return True, "Malformed email: consecutive or boundary dots detected"

    # 2. Domain checks
    if '.' not in domain:
        return True, "Domain lacks top-level domain extension"

    domain_parts = domain.split('.')
    tld = domain_parts[-1].lower()

    if tld in INVALID_SCRAPED_TLDS:
        return True, f"Invalid scraped top-level domain '.{tld}'"

    # 3. Detect text glued to domain from scraping (e.g. .comphone, .comwebsite)
    if GLUED_SCRAPE_WORDS_REGEX.search(domain):
        return True, f"Scraped text glued to domain name ('{domain}')"

    # 4. Public providers with single-letter or impossibly short usernames
    major_public_providers = {'gmail.com', 'googlemail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'}
    if domain in major_public_providers:
        # Gmail requires minimum 6 characters for usernames (except very old 1990s grandfathered google accounts)
        # Single or 2-char Gmails scraped from the web are almost always truncated scrapings
        if len(local_part) <= 2:
            return True, f"Suspiciously truncated username on {domain} ('{local_part}')"

    # 5. Non-alphanumeric leading/trailing chars
    if not local_part or not domain or not local_part[0].isalnum() or not domain[-1].isalnum():
        return True, "Email begins or ends with invalid non-alphanumeric character"

    return False, ""


def is_valid_syntax(email):
    """
    Deep RFC syntax validation using pyisemail with fallback to regex.
    Returns: (is_valid, reason)
    """
    if not email or len(email) > 254:
        return False, "Email exceeds RFC maximum length (254 chars)"

    if HAS_PYISEMAIL:
        try:
            diagnosis = pyisemail.is_email(email, diagnose=True)
            # ValidDiagnosis indicates valid email
            diagnosis_str = str(diagnosis)
            if 'VALID' not in diagnosis_str:
                return False, f"RFC Syntax Violation: {diagnosis_str}"
        except Exception as e:
            logger.debug(f"pyisemail check error: {e}")

    if not EMAIL_REGEX.match(email):
        return False, "Does not match standard RFC 5322 structure"

    return True, "Valid syntax"


def is_disposable(email):
    """Returns True if the email domain is a known disposable/temporary provider."""
    if '@' not in email:
        return False
    domain = email.split('@')[1].lower()
    return domain in DISPOSABLE_DOMAINS


def is_dangerous_spam_trap(email):
    """Returns True if the email prefix is abuse, spam, postmaster, or mailer-daemon."""
    if '@' not in email:
        return False
    prefix = email.split('@')[0].lower().split('+')[0]
    return prefix in DANGEROUS_PREFIXES


def is_role_based(email):
    """Returns True if the email is a generic role inbox (info@, admin@, etc.)."""
    if '@' not in email:
        return False
    prefix = email.split('@')[0].lower().split('+')[0]
    return prefix in ROLE_BASED_PREFIXES


@lru_cache(maxsize=2048)
def check_domain_mx_records(domain):
    """
    High-speed cached DNS check to verify whether a domain has active MX records.
    Uses dnspython with graceful fallback to standard library socket.
    Returns: (bool has_mx, str message)
    """
    domain = domain.strip().lower()

    # Major established providers always have MX records
    trusted_domains = {
        'gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.uk',
        'hotmail.com', 'outlook.com', 'live.com', 'msn.com',
        'icloud.com', 'me.com', 'aol.com', 'zoho.com', 'protonmail.com',
        'uniquetechcamp.org', 'example.com', 'example.org', 'example.net',
    }
    if domain in trusted_domains:
        return True, "Verified major email provider"

    # 1. Try dnspython for explicit MX records
    try:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3.0
        resolver.lifetime = 3.0

        answers = resolver.resolve(domain, 'MX')
        if answers:
            return True, f"Valid MX records resolved ({len(answers)} mail exchange servers)"
    except Exception:
        pass

    # 2. Fallback: Check if domain resolves to an IP address (A / AAAA record)
    try:
        addr_info = socket.getaddrinfo(domain, None)
        if addr_info:
            return True, "Domain resolves via A/AAAA records (Fallback)"
    except Exception:
        pass

    return False, f"Domain '{domain}' has no active MX or DNS records (Unreachable)"


def is_hard_bounce_error(error_str):
    """
    Inspects an SMTP exception or error string to detect if it constitutes a permanent 550 hard bounce.
    """
    if not error_str:
        return False
    err_lower = str(error_str).lower()
    return any(pat in err_lower for pat in HARD_BOUNCE_PATTERNS)


@lru_cache(maxsize=1024)
def check_mailbox_via_api(email, allow_open_disify=False):
    """
    Queries pluggable free email verification APIs if an API key is present in environment/settings,
    or optionally falls back to the free Disify open endpoint.
    Returns: (is_deliverable, reason) or (None, None) if inconclusive.
    """
    # Exclude reserved documentation domains
    if '@' in email:
        domain = email.split('@')[1].lower()
        if domain in {'example.com', 'example.org', 'example.net', 'test.com'}:
            return None, None

    # 1. Check for Abstract API (100 free/month)
    abstract_key = os.getenv('ABSTRACT_API_KEY') or os.getenv('EMAIL_VERIFICATION_API_KEY')
    if abstract_key:
        try:
            url = f"https://emailvalidation.abstractapi.com/v1/?api_key={abstract_key}&email={email}"
            resp = requests.get(url, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                deliverability = data.get('deliverability', '').upper()
                is_smtp_valid = data.get('is_smtp_valid', {}).get('value')
                if deliverability == 'UNDELIVERABLE' or is_smtp_valid is False:
                    return False, "AbstractAPI: Mailbox does not exist (Undeliverable)"
                if deliverability == 'DELIVERABLE' and is_smtp_valid is True:
                    return True, "AbstractAPI: Verified Deliverable"
        except Exception as e:
            logger.debug(f"Abstract API query failed: {e}")

    # 2. Check for ZeroBounce API (100 free/month)
    zerobounce_key = os.getenv('ZEROBOUNCE_API_KEY')
    if zerobounce_key:
        try:
            url = f"https://api.zerobounce.net/v2/validate?api_key={zerobounce_key}&email={email}"
            resp = requests.get(url, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                status = data.get('status', '').lower()
                sub_status = data.get('sub_status', '')
                if status == 'invalid':
                    return False, f"ZeroBounce: Mailbox invalid ({sub_status or 'does not exist'})"
                if status == 'valid':
                    return True, "ZeroBounce: Verified Mailbox"
        except Exception as e:
            logger.debug(f"ZeroBounce API query failed: {e}")

    # 3. Check for Emailable API (250 free credits)
    emailable_key = os.getenv('EMAILABLE_API_KEY')
    if emailable_key:
        try:
            url = f"https://api.emailable.com/v1/verify?api_key={emailable_key}&email={email}"
            resp = requests.get(url, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                state = data.get('state', '').lower()
                reason = data.get('reason', '')
                if state == 'undeliverable':
                    return False, f"Emailable: Undeliverable ({reason or 'rejected'})"
                if state == 'deliverable':
                    return True, "Emailable: Verified Deliverable"
        except Exception as e:
            logger.debug(f"Emailable API query failed: {e}")

    # 4. Free Open API Tier: Disify (Zero-cost, only when explicitly requested)
    if allow_open_disify:
        try:
            url = f"https://disify.com/api/email/{email}"
            resp = requests.get(url, timeout=2.0)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('format') is False:
                    return False, "Disify: Malformed format detected"
                if data.get('disposable') is True:
                    return False, "Disify: Disposable domain flagged"
                if data.get('dns') is False:
                    return False, "Disify: Domain has no DNS/MX records"
        except Exception as e:
            logger.debug(f"Disify check skipped/failed: {e}")

    return None, None


def check_mailbox_via_smtp_handshake(email):
    """
    Optional direct SMTP ping using py3-validate-email.
    Safely tests if mail server responds with 550 without sending an email.
    If server blocks port 25 or times out, returns None (inconclusive).
    """
    if not HAS_PY3_VALIDATE_EMAIL:
        return None, None

    try:
        # Pings SMTP server directly with a fast 3-second timeout
        is_valid = py3_validate_email(
            email_address=email,
            check_format=True,
            check_blacklist=False,
            check_dns=True,
            check_smtp=True,
            smtp_timeout=3
        )
        if is_valid is False:
            return False, "Mail server explicitly rejected mailbox (550 User Not Found via SMTP ping)"
        if is_valid is True:
            return True, "SMTP ping confirmed active mailbox"
    except Exception as e:
        logger.debug(f"SMTP ping skipped: {e}")

    return None, None


def verify_email_deliverability(email, check_dns=True, check_suppression=True, use_api=False, allow_open_disify=False):
    """
    Comprehensive multi-stage verification for cold scraped emails:
    1. Sanitization & typo auto-correction (gamil.com -> gmail.com)
    2. RFC 5321/5322 Syntax validation (via pyisemail + regex)
    3. Scraped email anomaly detection (bad TLDs, glued scraping tokens)
    4. Suppression List verification (previous hard bounces / manual blocks)
    5. Dangerous spam-trap check (abuse@, postmaster@, mailer-daemon@)
    6. Disposable email provider check (temp-mail, mailinator, etc.)
    7. DNS MX record validation (dnspython)
    8. Pluggable Free API & Open Verifier (Abstract API / ZeroBounce / Disify)
    9. Role-based accounts check (info@, admin@)

    Returns dict:
    {
        'is_safe': bool,
        'status': 'verified' | 'risky' | 'invalid' | 'suppressed',
        'reason': str,
        'cleaned_email': str,
        'was_fixed': bool,
    }
    """
    cleaned, was_fixed = clean_and_normalize_email(email)

    if not cleaned:
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': 'Empty email address',
            'cleaned_email': email,
            'was_fixed': False,
        }

    # 1. RFC Syntax Check
    syntax_ok, syntax_reason = is_valid_syntax(cleaned)
    if not syntax_ok:
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': syntax_reason,
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    # 2. Scraped Anomaly Check
    is_corrupt, anomaly_reason = detect_scrape_anomaly(cleaned)
    if is_corrupt:
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': anomaly_reason,
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    local_part, domain = cleaned.split('@', 1)

    # 3. Check suppression list (database)
    if check_suppression:
        try:
            from .models import EmailSuppressionList
            suppressed = EmailSuppressionList.objects.filter(email=cleaned).first()
            if suppressed:
                return {
                    'is_safe': False,
                    'status': 'suppressed',
                    'reason': f"Shield Blocked: {suppressed.get_reason_display()} ({suppressed.detail[:60] if suppressed.detail else 'Previously bounced'})",
                    'cleaned_email': cleaned,
                    'was_fixed': was_fixed,
                }
        except Exception as e:
            logger.warning(f"Could not query EmailSuppressionList: {e}")

    # 4. Check dangerous spam-trap
    if is_dangerous_spam_trap(cleaned):
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': f"Prohibited system/spam-trap prefix '{local_part}@'",
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    # 5. Check disposable domain
    if is_disposable(cleaned):
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': f"Disposable / temporary domain '{domain}'",
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    # 6. Check DNS MX records
    if check_dns:
        has_mx, mx_msg = check_domain_mx_records(domain)
        if not has_mx:
            return {
                'is_safe': False,
                'status': 'invalid',
                'reason': mx_msg,
                'cleaned_email': cleaned,
                'was_fixed': was_fixed,
            }

    # 7. Check Free Email Verification API / Open Endpoints
    if use_api:
        api_deliverable, api_reason = check_mailbox_via_api(cleaned, allow_open_disify=allow_open_disify)
        if api_deliverable is False:
            return {
                'is_safe': False,
                'status': 'invalid',
                'reason': api_reason,
                'cleaned_email': cleaned,
                'was_fixed': was_fixed,
            }

    # 8. Check role-based accounts (e.g. info@, support@)
    if is_role_based(cleaned):
        return {
            'is_safe': True,
            'status': 'risky',
            'reason': f"Role-based mailbox '{local_part}@' (Shared business inbox)",
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    return {
        'is_safe': True,
        'status': 'verified',
        'reason': 'Verified RFC syntax, valid DNS MX records & reputation clean',
        'cleaned_email': cleaned,
        'was_fixed': was_fixed,
    }
