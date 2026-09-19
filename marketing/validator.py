import re
import socket
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# RFC 5322 Compliant Email Regex
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
    'gmeil.com': 'gmail.com',
    'gmaill.co': 'gmail.com',
    # Yahoo
    'yaho.com': 'yahoo.com',
    'yahooo.com': 'yahoo.com',
    'yhaoo.com': 'yahoo.com',
    'yahoo.co': 'yahoo.com',
    'yaho.co': 'yahoo.com',
    # Microsoft Hotmail / Outlook
    'hotmial.com': 'hotmail.com',
    'hotmai.com': 'hotmail.com',
    'hotmaill.com': 'hotmail.com',
    'hotmial.co.uk': 'hotmail.co.uk',
    'outlok.com': 'outlook.com',
    'outloo.com': 'outlook.com',
    'outloock.com': 'outlook.com',
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
    'disposablemail.com', 'dropmail.me', 'getnada.com',
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


def clean_and_normalize_email(raw_email):
    """
    Sanitizes raw email strings scraped from web/Excel:
    - Strips leading/trailing punctuation, quotes, brackets (<, >)
    - Removes whitespace
    - Converts to lowercase
    - Corrects known domain typos (e.g. gamil.com -> gmail.com)
    Returns: (cleaned_email, was_typo_fixed)
    """
    if not raw_email:
        return '', False

    cleaned = str(raw_email).strip().lower()
    # Strip angle brackets, quotes, trailing semicolons or commas
    cleaned = cleaned.strip('<>()[]"\',;: \t\r\n')

    # Remove any internal whitespace
    cleaned = re.sub(r'\s+', '', cleaned)

    if '@' not in cleaned:
        return cleaned, False

    parts = cleaned.split('@')
    if len(parts) != 2:
        return cleaned, False

    local_part, domain_part = parts[0], parts[1]

    # Auto-correct common typos
    was_fixed = False
    if domain_part in DOMAIN_TYPOS:
        domain_part = DOMAIN_TYPOS[domain_part]
        was_fixed = True

    cleaned = f"{local_part}@{domain_part}"
    return cleaned, was_fixed


def is_valid_syntax(email):
    """Checks whether the email matches RFC syntax structure."""
    if not email or len(email) > 254:
        return False
    return bool(EMAIL_REGEX.match(email))


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
        'uniquetechcamp.org',
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
        # dnspython may raise NXDOMAIN, NoAnswer, Timeout, etc.
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


def verify_email_deliverability(email, check_dns=True, check_suppression=True):
    """
    Comprehensive multi-stage verification for cold scraped emails:
    1. Sanitization & typo auto-correction
    2. RFC 5322 Syntax validation
    3. Suppression List verification (previous hard bounces)
    4. Dangerous spam-trap check (abuse@, postmaster@)
    5. Disposable email provider check
    6. DNS MX record validation

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

    if not cleaned or not is_valid_syntax(cleaned):
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': 'Malformed email syntax (does not match RFC standards)',
            'cleaned_email': cleaned or email,
            'was_fixed': was_fixed,
        }

    local_part, domain = cleaned.split('@')

    # 1. Check suppression list (database)
    if check_suppression:
        try:
            from .models import EmailSuppressionList
            suppressed = EmailSuppressionList.objects.filter(email=cleaned).first()
            if suppressed:
                return {
                    'is_safe': False,
                    'status': 'suppressed',
                    'reason': f"Previously suppressed: {suppressed.get_reason_display()} ({suppressed.detail[:60]})",
                    'cleaned_email': cleaned,
                    'was_fixed': was_fixed,
                }
        except Exception as e:
            logger.warning(f"Could not query EmailSuppressionList: {e}")

    # 2. Check dangerous spam-trap
    if is_dangerous_spam_trap(cleaned):
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': f"Prohibited system/spam-trap address prefix '{local_part}'",
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    # 3. Check disposable domain
    if is_disposable(cleaned):
        return {
            'is_safe': False,
            'status': 'invalid',
            'reason': f"Disposable / throwaway domain '{domain}'",
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    # 4. Check DNS MX records
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

    # 5. Check role-based accounts (e.g. info@, support@)
    if is_role_based(cleaned):
        return {
            'is_safe': True,
            'status': 'risky',
            'reason': f"Role-based mailbox '{local_part}@' (General inbox)",
            'cleaned_email': cleaned,
            'was_fixed': was_fixed,
        }

    return {
        'is_safe': True,
        'status': 'verified',
        'reason': 'Valid RFC format & verified DNS MX records',
        'cleaned_email': cleaned,
        'was_fixed': was_fixed,
    }
