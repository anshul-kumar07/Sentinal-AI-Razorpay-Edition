"""
Sentinel AI 2.0 - Core Configuration & Threat Intelligence Dictionaries
Specialized for Razorpay, Indian Fintech, and Cyber Fraud Detection.
"""

import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Trusted Financial & Tech Brands (for Typosquatting / Lookalike Detection)
TRUSTED_BRANDS = {
    "razorpay": {
        "aliases": ["rzp", "razorpay"],
        "official_domains": ["razorpay.com", "rzp.io", "pages.razorpay.com", "api.razorpay.com", "razorpay.me"],
        "category": "Payment Gateway & Fintech",
        "official_support_email": "support@razorpay.com",
        "abuse_report_email": "abuse@razorpay.com"
    },
    "paytm": {
        "aliases": ["paytm"],
        "official_domains": ["paytm.com", "paytmbank.com", "p-y.tm"],
        "category": "Fintech & Payments"
    },
    "phonepe": {
        "aliases": ["phonepe"],
        "official_domains": ["phonepe.com", "phon.pe"],
        "category": "Fintech & UPI"
    },
    "googlepay": {
        "aliases": ["gpay", "googlepay"],
        "official_domains": ["pay.google.com", "g.co"],
        "category": "Fintech & Payments"
    },
    "sbi": {
        "aliases": ["sbi", "yono"],
        "official_domains": ["onlinesbi.sbi", "sbi.co.in", "sbicard.com"],
        "category": "Banking"
    },
    "hdfc": {
        "aliases": ["hdfc"],
        "official_domains": ["hdfcbank.com", "netbanking.hdfcbank.com"],
        "category": "Banking"
    },
    "icici": {
        "aliases": ["icici"],
        "official_domains": ["icicibank.com", "infinity.icicibank.com"],
        "category": "Banking"
    },
    "axis": {
        "aliases": ["axis"],
        "official_domains": ["axisbank.com"],
        "category": "Banking"
    },
    "npci": {
        "aliases": ["npci", "bhim"],
        "official_domains": ["npci.org.in", "bhimupi.org.in"],
        "category": "Payments Infrastructure"
    },
    "rbi": {
        "aliases": ["rbi"],
        "official_domains": ["rbi.org.in"],
        "category": "Central Bank / Regulatory"
    },
    "incometax": {
        "aliases": ["incometax", "itdept"],
        "official_domains": ["incometax.gov.in", "incometaxindiaefiling.gov.in"],
        "category": "Government Agency"
    },
    "amazon": {
        "aliases": ["amazon", "amzn"],
        "official_domains": ["amazon.in", "amazon.com", "amzn.in"],
        "category": "E-Commerce"
    },
    "flipkart": {
        "aliases": ["flipkart", "fkrt"],
        "official_domains": ["flipkart.com", "fkrt.it"],
        "category": "E-Commerce"
    }
}

# Known Legitimate NPCI UPI PSP Handles
LEGIT_UPI_HANDLES = {
    "okaxis", "okhdfcbank", "okicici", "oksbi", "paytm", "ibl", "ybl", 
    "axl", "upi", "apl", "rapl", "barodampay", "federal", "indus", 
    "kotak", "mahb", "pnb", "rbl", "aubank", "idfcbank", "dlb", "cnrb"
}

# High-Risk / Cheap TLDs often abused in phishing campaigns
SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".site", ".online", ".club", ".work", ".info", 
    ".click", ".live", ".space", ".buzz", ".monster", ".cfd", ".icu",
    ".vip", ".fit", ".rest", ".tk", ".ml", ".ga", ".cf", ".gq"
}

# High-Risk Phishing / Scam Keywords for Domain and Text
SUSPICIOUS_DOMAIN_KEYWORDS = [
    "login", "verify", "secure", "update", "kyc", "pan", "aadhar", "portal",
    "banking", "support", "helpdesk", "refund", "claim", "reward", "cashback",
    "bonus", "lottery", "instant-loan", "approval", "wallet", "gateway-verify",
    "razorpay-secure", "razorpay-pay", "rzp-support", "bill-payment", "electricity"
]

# Social Engineering Triggers (Cognitive Vectors)
URGENCY_TRIGGERS = [
    "immediately", "within 24 hours", "today only", "urgent", "last chance",
    "account suspended", "blocked", "deactivated", "legal action", "police complaint",
    "arrest warrant", "fine of", "electricity will be disconnected", "sim deactivated",
    "limited slots left", "hurry up", "offer expires"
]

FINANCIAL_LURES = [
    "scan qr to receive", "enter upi pin to receive", "refund processed", 
    "claim cashback", "won lottery", "daily payout", "work from home", 
    "youtube like task", "telegram task", "deposit required", "registration fee",
    "processing charge", "security deposit", "crypto doubling", "guaranteed profit"
]

AUTHORITY_IMPERSONATIONS = [
    "reserve bank of india", "rbi", "income tax department", "cyber cell",
    "mumbai police", "delhi police", "customs department", "courier customs",
    "sbi manager", "hdfc security team", "razorpay fraud desk", "hr manager"
]

# Scoring Weights
RISK_WEIGHTS = {
    "domain_spoofing": 35,
    "payment_trap": 30,
    "urgency_pressure": 20,
    "unverified_identity": 15
}

