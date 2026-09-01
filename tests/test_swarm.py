"""
Sentinel AI 2.0 - Automated Test Suite
Verifies all Autonomous Agents, OSINT Tools, Fintech Parsers, and the Swarm Orchestrator.
"""

import unittest
from core.orchestrator import SwarmOrchestrator
from tools.domain_tools import (
    extract_all_urls_and_domains,
    check_brand_typosquatting,
    analyze_domain_structure,
    levenshtein_distance
)
from tools.upi_tools import (
    extract_upi_vpas,
    check_payment_gateway_authenticity,
    detect_upi_collect_scam_pattern,
    detect_fake_kyc_banking_sms
)

class TestSentinelSwarm(unittest.TestCase):

    def setUp(self):
        self.orchestrator = SwarmOrchestrator()

    def test_levenshtein(self):
        self.assertEqual(levenshtein_distance("razorpay", "razorpay"), 0)
        self.assertEqual(levenshtein_distance("razorpqy", "razorpay"), 1)
        self.assertEqual(levenshtein_distance("rozorpay", "razorpay"), 1)

    def test_domain_tools(self):
        sample = "Please verify your account at https://razorpay-merchant-verification.xyz/login"
        extracted = extract_all_urls_and_domains(sample)
        self.assertTrue(len(extracted) >= 1)
        self.assertEqual(extracted[0]["domain"], "razorpay-merchant-verification.xyz")

        typosquat = check_brand_typosquatting("razorpay-verification.xyz")
        self.assertTrue(any(t["status"] == "BRAND_IMPERSONATION_EMBEDDED" for t in typosquat))

        structure = analyze_domain_structure("razorpay-verification.xyz")
        self.assertTrue(structure["structural_risk_score"] > 20)
        self.assertTrue(structure["is_suspicious_tld"])

    def test_payment_gateway_authenticity(self):
        legit = check_payment_gateway_authenticity("https://pages.razorpay.com/pl_test/receipt")
        self.assertEqual(legit["status"], "OFFICIAL_RAZORPAY_GATEWAY")
        self.assertEqual(legit["risk_score"], 0)

        fake = check_payment_gateway_authenticity("https://razorpay-secure-payment.xyz/checkout")
        self.assertEqual(fake["status"], "SPOOFED_RAZORPAY_GATEWAY")
        self.assertTrue(fake["risk_score"] >= 80)

    def test_upi_tools(self):
        sample = "Send Rs. 500 to support-rzp@okaxis or 9876543210@paytm"
        vpas = extract_upi_vpas(sample)
        self.assertEqual(len(vpas), 2)
        
        # Fake brand VPA check
        self.assertEqual(vpas[0]["impersonated_brand"], "razorpay")

        # UPI PIN paradox
        paradox = detect_upi_collect_scam_pattern("Enter UPI PIN to receive cashback refund")
        self.assertTrue(len(paradox) >= 1)
        self.assertEqual(paradox[0]["type"], "UPI_PIN_RECEIVE_PARADOX")

    def test_fake_razorpay_investigation(self):
        payload = (
            "Dear Merchant, your Razorpay settlement of Rs 48,250 is on hold! "
            "Verify immediately at: https://razorpay-merchant-verification.xyz/login?id=94821 "
            "- Razorpay Risk Desk (support-rzp@okaxis)"
        )
        report = self.orchestrator.run_investigation(payload)
        self.assertIn("Critical", report["overall_risk"])
        self.assertGreaterEqual(report["confidence_score"], 80)
        self.assertIn("cybercrime_complaint", report["autonomous_actions"])
        self.assertIn("razorpay_abuse_takedown", report["autonomous_actions"])

    def test_legit_razorpay_receipt(self):
        payload = (
            "Hi Anshul, your payment of Rs 1,499 via Razorpay was successful! "
            "View invoice at: https://razorpay.com/support/ "
            "Contact: support@razorpay.com"
        )
        report = self.orchestrator.run_investigation(payload)
        self.assertTrue("Safe" in report["overall_risk"] or "Low" in report["overall_risk"])
        self.assertLess(report["confidence_score"], 30)

    def test_dead_link_detection(self):
        payload = "View invoice at: https://pages.razorpay.com/non_existent_fake_invoice_9999"
        report = self.orchestrator.run_investigation(payload)
        self.assertTrue(report["confidence_score"] >= 40)
        self.assertTrue(any("404" in card["title"] or "Dead" in card["title"] for card in report["analysis"]))

if __name__ == "__main__":
    unittest.main()

