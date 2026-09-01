"""
Sentinel AI 2.0 - Domain & OSINT Inspection Tools
Provides network-level and algorithmic threat intelligence tools for URL and domain forensics.
"""

import re
import socket
import urllib.parse
from core.config import TRUSTED_BRANDS, SUSPICIOUS_TLDS, SUSPICIOUS_DOMAIN_KEYWORDS

def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def extract_all_urls_and_domains(text: str) -> list[dict]:
    """Extracts all URLs and naked domains from arbitrary text."""
    url_pattern = r"(?:https?:\/\/|www\.)[^\s/$.?#].[^\s]*"
    naked_domain_pattern = r"\b(?:[a-zA-Z0-9-]+\.)+(?:com|in|org|net|io|xyz|top|site|online|club|info|live|app|co|biz|me)\b"
    
    matches = []
    found_urls = set()

    for match in re.finditer(url_pattern, text, re.IGNORECASE):
        raw_url = match.group(0).rstrip(".,!?;:)\"'>")
        if raw_url not in found_urls:
            found_urls.add(raw_url)
            parsed = urllib.parse.urlparse(raw_url if "://" in raw_url else "http://" + raw_url)
            domain = parsed.netloc.lower()
            if ":" in domain:
                domain = domain.split(":")[0]
            matches.append({
                "raw": raw_url,
                "domain": domain,
                "path": parsed.path,
                "scheme": parsed.scheme or "http"
            })

    # Also search for naked domains not captured above
    for match in re.finditer(naked_domain_pattern, text, re.IGNORECASE):
        domain = match.group(0).lower().rstrip(".,!?;:)\"'>")
        if not any(domain in m["domain"] for m in matches):
            matches.append({
                "raw": f"http://{domain}",
                "domain": domain,
                "path": "",
                "scheme": "http"
            })

    return matches


def check_brand_typosquatting(domain: str) -> list[dict]:
    """
    Checks if a domain is a lookalike/typosquat of a trusted fintech or banking brand.
    e.g. razorpay-support.xyz, rzppay.com, sbi-kyc-portal.online
    """
    findings = []
    clean_domain = domain.lower()
    
    # Strip common subdomains like www.
    if clean_domain.startswith("www."):
        clean_domain = clean_domain[4:]

    for brand, info in TRUSTED_BRANDS.items():
        official_domains = info["official_domains"]
        
        # Exact match to official domain is legitimate
        if any(clean_domain == off or clean_domain.endswith("." + off) for off in official_domains):
            findings.append({
                "brand": brand,
                "status": "LEGITIMATE_OFFICIAL",
                "message": f"Verified official domain for {brand.upper()} ({info['category']})."
            })
            continue

        # Check if brand name is embedded in an unauthorized domain
        # e.g., razorpay-verification.site, login-razorpay.xyz
        if brand in clean_domain:
            findings.append({
                "brand": brand,
                "status": "BRAND_IMPERSONATION_EMBEDDED",
                "severity": "CRITICAL",
                "message": f"Brand '{brand.upper()}' appears inside an unauthorized domain structure ({domain}). Phishing lure detected."
            })
            continue

        # Check Levenshtein distance against official domain names (typosquatting)
        # e.g. razorpqy.com, rozorpay.com
        base_domain_name = clean_domain.split(".")[0]
        if len(base_domain_name) >= 4 and abs(len(base_domain_name) - len(brand)) <= 2:
            dist = levenshtein_distance(base_domain_name, brand)
            if 1 <= dist <= 2:
                findings.append({
                    "brand": brand,
                    "status": "TYPOSQUATTING_SIMILARITY",
                    "severity": "HIGH",
                    "distance": dist,
                    "message": f"Lookalike domain detected! '{base_domain_name}' is {dist} character edit distance from '{brand}'."
                })

    return findings


def analyze_domain_structure(domain: str) -> dict:
    """
    Performs deep heuristic and structural inspection on a domain.
    """
    domain = domain.lower()
    score = 0
    flags = []
    
    # Check TLD
    matched_tld = None
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            matched_tld = tld
            score += 25
            flags.append(f"Employs high-risk/low-reputation TLD ('{tld}') frequently utilized by automated phishing kits.")
            break

    # Check Hyphenation
    hyphen_count = domain.count("-")
    if hyphen_count >= 2:
        score += 20
        flags.append(f"Multiple hyphenated tokens ({hyphen_count} hyphens) indicate domain masking/impersonation.")
    elif hyphen_count == 1:
        score += 10
        flags.append("Hyphenated domain structure detected.")

    # Check Suspicious Keywords in domain
    detected_keywords = [kw for kw in SUSPICIOUS_DOMAIN_KEYWORDS if kw in domain]
    if detected_keywords:
        score += 20 * min(len(detected_keywords), 2)
        flags.append(f"Contains phishing/social-engineering keywords: {', '.join(detected_keywords)}.")

    # Check Subdomain Depth (e.g. secure.login.bank.portal.attacker.com)
    parts = domain.split(".")
    if len(parts) > 3:
        score += 15
        flags.append(f"Excessive subdomain nesting ({len(parts)} levels) used for visual deception on mobile viewports.")

    # Length & Entropy Heuristic
    if len(domain) > 30:
        score += 10
        flags.append(f"Unusually lengthy hostname ({len(domain)} chars) characteristic of dynamic DGA domains.")

    return {
        "domain": domain,
        "structural_risk_score": min(score, 100),
        "flags": flags,
        "is_suspicious_tld": bool(matched_tld),
        "matched_tld": matched_tld
    }


def resolve_dns_record(domain: str) -> dict:
    """
    Safe DNS resolver tool. Attempts live lookup with graceful timeout.
    """
    try:
        ip = socket.gethostbyname(domain)
        return {
            "resolved": True,
            "ip_address": ip,
            "status": "HOST_ACTIVE"
        }
    except Exception as e:
        return {
            "resolved": False,
            "ip_address": None,
            "status": "UNRESOLVED_OR_OFFLINE",
            "error": str(e)
        }

