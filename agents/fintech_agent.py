"""
Sentinel AI 2.0 - Fintech & Payment Forensic Agent
Specialized for Razorpay Gateways, UPI VPA Forensics, Collect Request Traps, and Banking Phishing.
"""

from agents.base_agent import BaseAgent
from tools.upi_tools import (
    extract_upi_vpas,
    parse_upi_deep_links,
    check_payment_gateway_authenticity,
    detect_upi_collect_scam_pattern,
    detect_fake_kyc_banking_sms
)

class FintechAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Fintech & Payment Forensic Agent",
            role="UPI, Razorpay Gateway & Financial Lure Forensics",
            icon="💳"
        )

    def run(self, input_text: str, context: dict) -> dict:
        self.reset()
        self.status = "RUNNING"
        self.log("THOUGHT", "Analyzing financial transaction vectors, payment identifiers, and settlement mechanics...")

        fintech_risk_score = 0
        explanations = []
        is_payment_scam = False

        # 1. UPI VPA Inspection Tool
        vpas = extract_upi_vpas(input_text)
        self.log("TOOL_CALL", f"Invoked extract_upi_vpas() -> Found {len(vpas)} VPA identifier(s).", vpas)

        for vpa_info in vpas:
            vpa = vpa_info["vpa"]
            if vpa_info["impersonated_brand"]:
                brand = vpa_info["impersonated_brand"]
                self.log("WARNING", f"VPA '{vpa}' uses personal PSP handle (@{vpa_info['handle']}) while impersonating '{brand.upper()}'!")
                fintech_risk_score = max(fintech_risk_score, 80)
                is_payment_scam = True
                explanations.append({
                    "title": f"Spoofed Merchant UPI VPA ({brand.upper()})",
                    "text": f"VPA '{vpa}' masquerades as official {brand.title()} entity on a personal bank handle (@{vpa_info['handle']})."
                })
            elif vpa_info["is_phone_number_vpa"]:
                self.log("OBSERVATION", f"Personal mobile-linked VPA detected: {vpa}")

        # 2. UPI Deep Link Parser Tool
        deep_links = parse_upi_deep_links(input_text)
        if deep_links:
            self.log("TOOL_CALL", f"Invoked parse_upi_deep_links() -> Discovered {len(deep_links)} direct UPI pay link(s).", deep_links)

        # 3. UPI Collect Scam / "Enter PIN to Receive" Paradox Tool
        collect_traps = detect_upi_collect_scam_pattern(input_text)
        self.log("TOOL_CALL", "Invoked detect_upi_collect_scam_pattern()", collect_traps)
        if collect_traps:
            for trap in collect_traps:
                fintech_risk_score = max(fintech_risk_score, 90)
                is_payment_scam = True
                self.log("WARNING", f"CRITICAL: {trap['law']}")
                explanations.append({
                    "title": "UPI Reversal / PIN Collect Trap",
                    "text": f"{trap['explanation']} {trap['law']}"
                })

        # Check if all links in context are verified official enterprise endpoints
        has_domains = "osint" in context and bool(context["osint"].get("domains_analyzed"))
        all_domains_official = False
        if has_domains:
            domain_reports = context["osint"]["domains_analyzed"]
            all_domains_official = all(
                any(t.get("status") == "LEGITIMATE_OFFICIAL" for t in d.get("typosquat", []))
                for d in domain_reports
            ) and context["osint"].get("osint_risk_score", 0) == 0

        # 4. Banking KYC / Electricity Threat Patterns Tool
        banking_traps = detect_fake_kyc_banking_sms(input_text, is_official_domain=all_domains_official)
        self.log("TOOL_CALL", "Invoked detect_fake_kyc_banking_sms()", banking_traps)
        if banking_traps:
            for bt in banking_traps:
                fintech_risk_score = max(fintech_risk_score, 75)
                is_payment_scam = True
                explanations.append({
                    "title": bt["type"].replace("_", " ").title(),
                    "text": bt["explanation"]
                })
        elif all_domains_official:
            self.log("OBSERVATION", "Compliance / administrative message links strictly to verified official domain infrastructure.")

        # 5. Payment Gateway Authenticity Tool (Razorpay specific)
        urls_to_check = []
        if "osint" in context and "domains_analyzed" in context["osint"]:
            for d in context["osint"]["domains_analyzed"]:
                urls_to_check.append(d["domain"])

        for item in urls_to_check:
            gateway_check = check_payment_gateway_authenticity(item)
            if gateway_check.get("relevant"):
                self.log("TOOL_CALL", f"Invoked check_payment_gateway_authenticity('{item}')", gateway_check)
                if gateway_check["status"] == "SPOOFED_RAZORPAY_GATEWAY":
                    fintech_risk_score = max(fintech_risk_score, gateway_check["risk_score"])
                    is_payment_scam = True
                    explanations.append({
                        "title": "Fake Razorpay Gateway Endpoint",
                        "text": gateway_check["message"]
                    })
                elif gateway_check["status"] == "OFFICIAL_RAZORPAY_GATEWAY":
                    self.log("OBSERVATION", "Legitimate Razorpay payment infrastructure confirmed.")
                    explanations.append({
                        "title": "Authentic Razorpay Gateway",
                        "text": gateway_check["message"]
                    })

        self.log("DECISION", f"Fintech Agent finalized payment forensics. Risk Score: {fintech_risk_score}/100.")
        self.status = "COMPLETED"

        return {
            "vpas_analyzed": vpas,
            "deep_links": deep_links,
            "fintech_risk_score": min(fintech_risk_score, 100),
            "is_payment_scam": is_payment_scam,
            "explanations": explanations
        }

