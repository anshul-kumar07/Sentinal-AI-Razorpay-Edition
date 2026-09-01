"""
Sentinel AI 2.0 - Autonomous Remediation & Action Agent
Synthesizes cross-agent telemetry into actionable defense countermeasures:
CERT-In Complaints, Razorpay Abuse Takedowns, and End-User Safety Playbooks.
"""

from agents.base_agent import BaseAgent
from tools.reporting_tools import (
    generate_cybercrime_complaint_payload,
    generate_razorpay_abuse_takedown_notice,
    generate_safety_playbook
)

class RemediationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Autonomous Action & Defense Agent",
            role="Incident Response, Takedown Notices & Safety Playbooks",
            icon="🛡️"
        )

    def run(self, input_text: str, context: dict) -> dict:
        self.reset()
        self.status = "RUNNING"
        self.log("THOUGHT", "Synthesizing cross-agent telemetry to formulate autonomous incident response actions...")

        overall_risk = context.get("overall_risk", "Low")
        vectors = context.get("detected_vectors", [])
        
        # Identify if Razorpay or another specific brand was spoofed
        spoofed_domain = ""
        if "osint" in context and context["osint"].get("domains_analyzed"):
            for d in context["osint"]["domains_analyzed"]:
                if d.get("structure", {}).get("structural_risk_score", 0) > 30:
                    spoofed_domain = d.get("domain", "")
                    break

        # 1. Cybercrime Complaint Generation Tool
        complaint_payload = generate_cybercrime_complaint_payload(context, input_text)
        self.log("TOOL_CALL", "Invoked generate_cybercrime_complaint_payload() -> Formatted for cybercrime.gov.in.")

        # 2. Razorpay Abuse Takedown Tool
        takedown_payload = generate_razorpay_abuse_takedown_notice(context, spoofed_domain)
        self.log("TOOL_CALL", "Invoked generate_razorpay_abuse_takedown_notice() -> Addressed to abuse@razorpay.com.")

        # 3. User Safety Playbook Tool
        safety_playbook = generate_safety_playbook(overall_risk, vectors)
        self.log("TOOL_CALL", f"Invoked generate_safety_playbook() -> Built {len(safety_playbook)} step defense protocol.")

        self.log("DECISION", "Remediation Agent generated verifiable incident response package.")
        self.status = "COMPLETED"

        return {
            "complaint_payload": complaint_payload,
            "takedown_payload": takedown_payload,
            "safety_playbook": safety_playbook
        }

