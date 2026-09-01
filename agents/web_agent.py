"""
Sentinel AI 2.0 - Live Web & Content Forensic Agent
Actively connects to websites in real-time to inspect HTTP status, verify live existence,
extract page content, and detect credential-harvesting forms.
"""

from agents.base_agent import BaseAgent
from tools.web_probe_tools import probe_live_url

class LiveWebAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Live Web & Content Inspector Agent",
            role="Real-Time HTTP Probing, DOM Forensics & Live Page Verification",
            icon="🌐"
        )

    def run(self, input_text: str, context: dict) -> dict:
        self.reset()
        self.status = "RUNNING"
        self.log("THOUGHT", "Scanning context for live URL endpoints to initiate real-time web probing and content forensics...")

        extracted_targets = []
        if "osint" in context and "domains_analyzed" in context["osint"]:
            for d in context["osint"]["domains_analyzed"]:
                extracted_targets.append(d["domain"])

        if not extracted_targets:
            self.log("OBSERVATION", "No external URLs present in payload for live web probing.")
            self.status = "COMPLETED"
            return {
                "probed_results": [],
                "web_risk_score": 0,
                "explanations": []
            }

        probed_results = []
        web_risk_score = 0
        explanations = []

        for target in extracted_targets:
            self.log("THOUGHT", f"Establishing live HTTPS connection to probe '{target}'...")
            
            probe_result = probe_live_url(target)
            self.log("TOOL_CALL", f"Invoked probe_live_url('{target}') -> HTTP Status: {probe_result.get('status_code', 'N/A')}", probe_result)

            if not probe_result["reachable"]:
                error_type = probe_result.get("error_type", "OFFLINE")
                self.log("WARNING", f"Target '{target}' is UNREACHABLE / OFFLINE ({error_type}): {probe_result.get('page_summary')}")
                web_risk_score = max(web_risk_score, 45)
                explanations.append({
                    "title": "Unreachable / Inactive Domain (HTTP Error)",
                    "text": f"The link '{target}' failed live connection probes ({error_type}). The server is offline or unreachable."
                })

            elif probe_result.get("is_404_or_dead"):
                self.log("WARNING", f"DEAD LINK DETECTED: '{target}' returned HTTP 404 Not Found.")
                web_risk_score = max(web_risk_score, 50)
                explanations.append({
                    "title": "Dead / Non-Existent Web Link (HTTP 404)",
                    "text": f"The link '{target}' returned HTTP 404 (Page Not Found). The page does not exist on the server."
                })

            else:
                title = probe_result.get("page_title", "")
                summary = probe_result.get("page_summary", "")
                dom = probe_result.get("dom_forensics", {})
                
                self.log("OBSERVATION", f"Target is LIVE (HTTP {probe_result['status_code']}). Page Title: '{title}'. Summary: {summary}.")
                
                # Check for Phishing / Credential harvesting in DOM on unverified domain
                is_official = False
                if "osint" in context and context["osint"].get("domains_analyzed"):
                    for d in context["osint"]["domains_analyzed"]:
                        if d["domain"] == target:
                            is_official = any(t.get("status") == "LEGITIMATE_OFFICIAL" for t in d.get("typosquat", []))
                            break

                if dom.get("has_password_field") and not is_official:
                    web_risk_score = max(web_risk_score, 90)
                    self.log("WARNING", f"CRITICAL PHISHING DOM: Password input field detected on unauthorized domain '{target}'!")
                    explanations.append({
                        "title": "Active Credential Harvesting Form (DOM Forensic)",
                        "text": f"The live webpage on '{target}' contains password input fields on an unauthorized domain designed to steal credentials."
                    })
                elif is_official:
                    explanations.append({
                        "title": "Live Verified Enterprise Webpage",
                        "text": f"Live webpage confirmed active (HTTP 200). Content: {summary} (Title: '{title}')."
                    })
                else:
                    explanations.append({
                        "title": "Live Third-Party Webpage",
                        "text": f"Webpage is active (HTTP {probe_result['status_code']}). Title: '{title}'. Summary: {summary}."
                    })

            probed_results.append(probe_result)

        self.log("DECISION", f"Live Web Inspector finalized page forensics. Web Risk Score: {web_risk_score}/100.")
        self.status = "COMPLETED"

        return {
            "probed_results": probed_results,
            "web_risk_score": min(web_risk_score, 100),
            "explanations": explanations
        }

