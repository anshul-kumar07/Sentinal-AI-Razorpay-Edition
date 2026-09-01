"""
Sentinel AI 2.0 - Fintech & UPI Forensics Tools
Provides specialized tools for UPI VPAs, Payment Gateways, QR Collect Reversals, and Banking SMS Forensics.
"""

import re
import urllib.parse
from core.config import LEGIT_UPI_HANDLES, TRUSTED_BRANDS

def extract_upi_vpas(text: str) -> list[dict]:
    """
    Extracts and parses all UPI Virtual Payment Addresses (VPAs) from text.
    Format: username@handle (e.g., razorpay.support@oksbi, payment@paytm, 9876543210@ybl)
    Ignores standard email addresses like user@razorpay.com.
    """
    # Exclude emails where @handle is followed by .tld (e.g. @razorpay.com)
    vpa_pattern = r"\b([a-zA-Z0-9.\-_]+)@([a-zA-Z0-9]+)(?!\.[a-zA-Z]{2,})\b"
    results = []
    
    suspicious_vpa_keywords = ["support", "refund", "desk", "service", "care", "official", "helpdesk", "verification", "manager", "admin"]

    for match in re.finditer(vpa_pattern, text):
        full_vpa = match.group(0).lower()
        username = match.group(1).lower()
        handle = match.group(2).lower()
        
        # Filter out common email domains
        common_email_tlds = {"com", "in", "org", "net", "edu", "gov", "co", "io", "xyz", "ai", "me"}
        if handle in common_email_tlds:
            continue
            
        is_known_psp = handle in LEGIT_UPI_HANDLES
        
        # Check if username impersonates a brand or uses fake corporate authority words
        impersonated_brand = None
        for brand, info in TRUSTED_BRANDS.items():
            aliases = info.get("aliases", [brand])
            if any(alias in username for alias in aliases):
                impersonated_brand = brand
                break

        if not impersonated_brand and any(kw in username for kw in suspicious_vpa_keywords):
            impersonated_brand = "Payment/Support Service"

        is_phone_vpa = bool(re.fullmatch(r"[6-9]\d{9}", username))

        results.append({
            "vpa": full_vpa,
            "username": username,
            "handle": handle,
            "is_known_psp": is_known_psp,
            "impersonated_brand": impersonated_brand,
            "is_phone_number_vpa": is_phone_vpa
        })

    return results


def parse_upi_deep_links(text: str) -> list[dict]:
    """
    Parses upi://pay URI schemes often embedded in QR codes or WhatsApp buttons.
    """
    upi_uri_pattern = r"upi:\/\/pay\?[^\s\"'>]+"
    results = []
    
    for match in re.finditer(upi_uri_pattern, text, re.IGNORECASE):
        uri = match.group(0)
        parsed = urllib.parse.urlparse(uri)
        params = urllib.parse.parse_qs(parsed.query)
        
        pa = params.get("pa", [""])[0] # Payee VPA
        pn = params.get("pn", [""])[0] # Payee Name
        am = params.get("am", [""])[0] # Amount
        tn = params.get("tn", [""])[0] # Transaction Note
        
        results.append({
            "raw_uri": uri,
            "payee_vpa": pa,
            "payee_name": pn,
            "amount": am,
            "transaction_note": tn
        })

    return results


def check_payment_gateway_authenticity(url_or_domain: str) -> dict:
    """
    Validates whether a payment gateway URL or domain is genuinely hosted by Razorpay or a spoof.
    """
    clean = url_or_domain.lower().strip()
    
    if "razorpay" not in clean and "rzp" not in clean:
        return {"relevant": False}

    # Extract hostname if full URL
    if "://" in clean:
        parsed = urllib.parse.urlparse(clean)
        domain = parsed.netloc.split(":")[0]
    else:
        domain = clean.split("/")[0]

    official_domains = ["razorpay.com", "rzp.io", "pages.razorpay.com", "api.razorpay.com", "razorpay.me"]
    
    is_official = (domain in official_domains) or any(domain.endswith("." + off) for off in ["razorpay.com", "rzp.io"])
    
    if is_official:
        return {
            "relevant": True,
            "status": "OFFICIAL_RAZORPAY_GATEWAY",
            "risk_score": 0,
            "message": f"Verified authentic Razorpay endpoint ({domain})."
        }
    else:
        return {
            "relevant": True,
            "status": "SPOOFED_RAZORPAY_GATEWAY",
            "risk_score": 90,
            "severity": "CRITICAL",
            "message": f"CRITICAL FRAUD ALERT: '{domain}' is impersonating Razorpay Payment Gateway on an unauthorized domain!"
        }


def detect_upi_collect_scam_pattern(text: str) -> list[dict]:
    """
    Detects classic Indian payment reversal / UPI PIN scam lures.
    Rule: 'Enter UPI PIN to receive money' is physically impossible in UPI architecture.
    """
    text_lower = text.lower()
    findings = []

    pin_receive_patterns = [
        r"enter\s+(?:your\s+)?(?:upi\s+)?p[i|1|l]?n\s+to\s+(?:receive|credit|claim|accept|get)",
        r"scan\s+(?:this\s+)?(?:the\s+)?(?:attached\s+)?qr\s+(?:code\s+)?(?:in\s+.*?\s+)?to\s+(?:receive|get|claim|accept)\s+(?:money|cashback|refund|rs|\u20b9)?",
        r"approve\s+(?:request|collect|payment)\s+to\s+(?:receive|get)\s+refund",
        r"send\s+(?:rs|\u20b9|\$)?\s*\d+\s+to\s+activate\s+(?:refund|account|wallet|kyc)",
    ]

    matched = any(re.search(p, text_lower) for p in pin_receive_patterns)

    # General heuristic fallbacks for OCR noise
    if not matched:
        has_qr_scan = "qr" in text_lower and ("scan" in text_lower or "code" in text_lower)
        has_receive_intent = any(w in text_lower for w in ["receive", "claim", "accept", "refund", "cashback"])
        has_pin_mention = any(w in text_lower for w in ["pin", " pn", "upi pin", "6-digit"])
        if (has_qr_scan and has_receive_intent) or (has_pin_mention and has_receive_intent):
            matched = True

    if matched:
        findings.append({
            "type": "UPI_PIN_RECEIVE_PARADOX",
            "severity": "CRITICAL",
            "law": "NPCI UPI Architectural Rule: UPI PIN is ONLY entered to DEBIT your account. Entering a PIN will instantly drain funds.",
            "explanation": "Scammer is masquerading a DEBIT collect request as a cashback/refund claim."
        })

    return findings


def detect_fake_kyc_banking_sms(text: str, is_official_domain: bool = False) -> list[dict]:
    """
    Detects standard Indian banking / utility threat patterns (SBI YONO, HDFC, Electricity bill).
    If communication is verified to use official domain endpoints, administrative notices are allowed.
    """
    if is_official_domain:
        return []

    text_lower = text.lower()
    findings = []

    # Bank KYC Block Threat
    if any(k in text_lower for k in ["kyc", "pan", "aadhar", "yono", "netbanking"]) and \
       any(w in text_lower for w in ["blocked", "suspended", "deactivated", "expire", "hold", "stop"]):
        findings.append({
            "type": "BANK_KYC_SUSPENSION_LURE",
            "severity": "HIGH",
            "explanation": "Standard panic-inducing Bank/KYC suspension template designed to force immediate credential theft."
        })

    # Electricity / Utility Bill Disconnection Scam
    if ("electricity" in text_lower or "power" in text_lower or "bill" in text_lower) and \
       ("disconnected" in text_lower or "cut off" in text_lower or "officer" in text_lower):
        findings.append({
            "type": "ELECTRICITY_BILL_DISCONNECTION_SCAM",
            "severity": "HIGH",
            "explanation": "Urgent utility disconnection scam designed to make victims call a fake officer or install remote desktop apps (AnyDesk/TeamViewer)."
        })

    return findings

