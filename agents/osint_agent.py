"""
Sentinel AI 2.0 - OSINT & Network Intelligence Agent
Autonomously interrogates domains, URL structures, typosquatting vectors, and network infrastructure.
"""

from agents.base_agent import BaseAgent
from tools.domain_tools import (
    extract_all_urls_and_domains,
    check_brand_typosquatting,
    analyze_domain_structure,
    resolve_dns_record
)

class OSINTAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="OSINT & Network Intelligence Agent",
            role="Domain, DNS & Brand Spoofing Forensics",
            icon="🔍"
        )

    def run(self, input_text: str, context: dict) -> dict:
        self.reset()
        self.status = "RUNNING"
        self.log("THOUGHT", "Scanning input payload for embedded links, shortened URLs, and naked domain references...")

        # 1. URL Extraction Tool
        extracted_targets = extract_all_urls_and_domains(input_text)
        self.log("TOOL_CALL", f"Invoked extract_all_urls_and_domains() -> Discovered {len(extracted_targets)} target(s).", {
            "targets": [t["domain"] for t in extracted_targets]
        })

        if not extracted_targets:
            self.log("OBSERVATION", "No explicit domains or external URLs found in payload.")
            self.status = "COMPLETED"
            return {
                "domains_analyzed": [],
                "osint_risk_score": 0,
                "flags": [],
                "explanations": [],
                "is_spoofed_brand": False
            }

        domain_reports = []
        accumulated_risk = 0
        explanations = []
        is_spoofed_brand = False
        spoofed_brands = []

        for target in extracted_targets:
            domain = target["domain"]
            self.log("THOUGHT", f"Performing deep OSINT heuristic on domain target: '{domain}'...")

            # 2. Typosquatting & Brand Impersonation Tool
            typosquat_results = check_brand_typosquatting(domain)
            self.log("TOOL_CALL", f"Invoked check_brand_typosquatting('{domain}')", typosquat_results)

            # 3. Structural & TLD Inspection Tool
            structural_report = analyze_domain_structure(domain)
            self.log("TOOL_CALL", f"Invoked analyze_domain_structure('{domain}')", structural_report)

            # 4. Safe DNS Resolution Tool
            dns_report = resolve_dns_record(domain)
            self.log("TOOL_CALL", f"Invoked resolve_dns_record('{domain}') -> Host Status: {dns_report['status']}")

            # Analyze findings for this domain
            is_legit_brand = any(t.get("status") == "LEGITIMATE_OFFICIAL" for t in typosquat_results)
            brand_phishing = [t for t in typosquat_results if t.get("status") in ["BRAND_IMPERSONATION_EMBEDDED", "TYPOSQUATTING_SIMILARITY"]]

            if is_legit_brand:
                self.log("OBSERVATION", f"Domain '{domain}' verified as an authentic official enterprise endpoint.")
                explanations.append({
                    "title": "Verified Official Domain",
                    "text": f"'{domain}' matches official registry for trusted brand."
                })
            elif brand_phishing:
                is_spoofed_brand = True
                for bp in brand_phishing:
                    spoofed_brands.append(bp["brand"])
                    accumulated_risk = max(accumulated_risk, 85)
                    self.log("WARNING", f"CRITICAL SPOOFING: {bp['message']}")
                    explanations.append({
                        "title": f"Phishing Lookalike ({bp['brand'].upper()})",
                        "text": bp["message"]
                    })
            else:
                if structural_report["structural_risk_score"] > 0:
                    accumulated_risk = max(accumulated_risk, structural_report["structural_risk_score"])
                    for flag in structural_report["flags"]:
                        explanations.append({
                            "title": "Suspicious Domain Signature",
                            "text": flag
                        })

            domain_reports.append({
                "domain": domain,
                "typosquat": typosquat_results,
                "structure": structural_report,
                "dns": dns_report
            })

        self.log("DECISION", f"OSINT Agent finalized evaluation. Calculated Network Risk Score: {accumulated_risk}/100.")
        self.status = "COMPLETED"

        return {
            "domains_analyzed": domain_reports,
            "osint_risk_score": min(accumulated_risk, 100),
            "is_spoofed_brand": is_spoofed_brand,
            "spoofed_brands": list(set(spoofed_brands)),
            "explanations": explanations
        }

