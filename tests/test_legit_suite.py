"""Test suite specifically for Ground Truth Safe & Legitimate Messages."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from core.orchestrator import SwarmOrchestrator

s = SwarmOrchestrator()

samples = [
    ("Genuine Razorpay Receipt", "Hi Anshul, your payment of Rs 1,499 to Urban Company via Razorpay was successful! Payment ID: pay_Nq73Ks81JkLm90. View invoice at: https://razorpay.com/support/ Contact: support@razorpay.com"),
    ("Genuine Bank Debit Alert", "Dear Customer, your A/C ending 4910 has been debited by INR 850.00 on 27-Aug-2026 at STARBUCKS COFFEE. Available balance: INR 42,190.00. - HDFC Bank"),
    ("Genuine Bank OTP SMS", "948102 is your secret OTP for transaction of INR 2,450.00 at AMAZON INDIA on your HDFC Bank Card ending 1084. OTP is valid for 5 mins. Do not share OTP with anyone including bank officials."),
    ("Genuine Amazon Delivery Alert", "Your Amazon package with tracking #AMZN9481920 is out for delivery today by 8 PM. Track your order on the official Amazon app: https://amazon.in"),
    ("Genuine HR Interview Invite", "Dear Anshul, Thank you for applying for the Software Engineering role at Razorpay. We would like to invite you for a 45-minute technical discussion over Google Meet. Please find the meeting invite on your calendar. Regards, Talent Acquisition Team, Razorpay.")
]

for name, text in samples:
    res = s.run_investigation(text)
    print(f"\n[SCENARIO: {name}]")
    print(f"Verdict: {res['overall_risk']} | Badge: {res['risk_badge']} | Score: {res['confidence_score']}%")
    print("Evidence Breakdown:")
    for card in res["analysis"]:
        print(f"  * {card['title']}: {card['text']}")
