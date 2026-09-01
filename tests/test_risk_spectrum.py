"""
Test Suite for Calibrated Risk Spectrum (0%, 20%, 35%, 50%, 75%, 95%)
Demonstrates how each agent's specialized intelligence uniquely influences the consensus.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from core.orchestrator import SwarmOrchestrator

s = SwarmOrchestrator()

scenarios = [
    (
        "LEVEL 1 [0% - VERIFIED SAFE]: Authentic Razorpay Receipt (Live 200 OK)",
        "Hi Anshul, your payment of Rs 1,499 via Razorpay was successful! View invoice: https://razorpay.com/support/ Contact: support@razorpay.com"
    ),
    (
        "LEVEL 2 [20% - LOW / MINIMAL ANOMALY]: Verified Official Portal with Soft Urgency",
        "Dear Merchant, your annual merchant compliance review is scheduled. Please review your account settings at https://accounts.razorpay.com/auth/?auth_intent=login within the next 7 days."
    ),
    (
        "LEVEL 3 [35% - MEDIUM / SUSPICIOUS]: Unverified Generic Link with Marketing Urgency",
        "Complete 3 daily feedback surveys on https://daily-reward-tasks.org/survey to claim retail vouchers. Offer valid for 24 hours only."
    ),
    (
        "LEVEL 4 [50% - HIGH RISK]: Dead Phishing Link + Suspicious TLD (.xyz)",
        "India Post: Package #IN83910 cannot be delivered. Pay Rs 25 re-delivery fee at https://indiapost-address-update.xyz/pay within 12 hours."
    ),
    (
        "LEVEL 5 [75% - SEVERE THREAT]: Brand Typosquatting Phishing Gateway",
        "Dear Merchant, your Razorpay account is flagged. Re-verify merchant login at https://razorpayy-secure-login.com to avoid account termination."
    ),
    (
        "LEVEL 6 [95% - CRITICAL FRAUD]: Multi-Vector Attack (Fake Gateway + UPI PIN Trap + Police Threat)",
        "URGENT: Delhi Police Cyber Crime & Razorpay Alert. Fraudulent settlement of Rs 48,250 on your account. To prevent immediate digital arrest warrant, verify at https://razorpay-merchant-verification.xyz and enter UPI PIN on GooglePay to refund@okaxis within 2 hours."
    )
]

print("=" * 80)
print("  SENTINEL AI 2.0 - MULTI-AGENT CALIBRATED RISK SPECTRUM TEST")
print("=" * 80)

for name, text in scenarios:
    res = s.run_investigation(text)
    print(f"\n>>> {name}")
    print(f"Verdict: {res['overall_risk']} | Badge: [{res['risk_badge']}] | Composite Confidence: {res['confidence_score']}%")
    print(f"Agent Vectors: OSINT: {res['vectors']['osint_risk']}% | Web: {res['vectors']['web_risk']}% | Fintech: {res['vectors']['fintech_risk']}% | Cognitive: {res['vectors']['cognitive_risk']}%")
    print("Agent Findings Breakdown:")
    for card in res["analysis"]:
        print(f"  * {card['title']}: {card['text']}")

