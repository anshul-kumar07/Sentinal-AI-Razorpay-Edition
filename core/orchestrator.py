"""
Sentinel AI 2.0 - Multi-Agent Orchestrator & Risk Arbitrator
Orchestrates agent swarm lifecycle, maintains blackboard memory, arbitrates risk consensus,
and yields live telemetry stream.
"""

import time
from typing import Generator
from agents.osint_agent import OSINTAgent
from agents.web_agent import LiveWebAgent
from agents.fintech_agent import FintechAgent
from agents.cognitive_agent import CognitiveAgent
from agents.remediation_agent import RemediationAgent

class SwarmOrchestrator:
    def __init__(self):
        self.osint_agent = OSINTAgent()
        self.web_agent = LiveWebAgent()
        self.fintech_agent = FintechAgent()
        self.cognitive_agent = CognitiveAgent()
        self.remediation_agent = RemediationAgent()

    def run_investigation(self, input_text: str) -> dict:
        """
        Executes a complete multi-agent investigation synchronously.
        """
        context = {
            "input_text": input_text,
            "timestamp": time.time()
        }

        # Step 1: OSINT Agent
        osint_res = self.osint_agent.run(input_text, context)
        context["osint"] = osint_res

        # Step 2: Live Web & Content Inspector Agent
        web_res = self.web_agent.run(input_text, context)
        context["web"] = web_res

        # Step 3: Cognitive Reasoning Agent
        cognitive_res = self.cognitive_agent.run(input_text, context)
        context["cognitive"] = cognitive_res

        # Step 4: Fintech & Payment Forensics Agent
        fintech_res = self.fintech_agent.run(input_text, context)
        context["fintech"] = fintech_res

        # Step 5: Consensus & Risk Arbitration
        arbitration = self._arbitrate_risk(context)
        context.update(arbitration)

        # Step 6: Autonomous Remediation Agent
        remediation_res = self.remediation_agent.run(input_text, context)
        context["remediation"] = remediation_res

        # Step 7: Compile Unified Multi-Agent Dossier
        all_traces = (
            self.osint_agent.thought_log +
            self.web_agent.thought_log +
            self.cognitive_agent.thought_log +
            self.fintech_agent.thought_log +
            self.remediation_agent.thought_log
        )

        return {
            "overall_risk": context["overall_risk"],
            "risk_badge": context["risk_badge"],
            "confidence_score": context["confidence_score"],
            "analysis": context["analysis"],
            "recommendation": context["recommendation"],
            "vectors": {
                "osint_risk": osint_res.get("osint_risk_score", 0),
                "web_risk": web_res.get("web_risk_score", 0),
                "fintech_risk": fintech_res.get("fintech_risk_score", 0),
                "cognitive_risk": cognitive_res.get("cognitive_risk_score", 0)
            },
            "autonomous_actions": {
                "cybercrime_complaint": remediation_res["complaint_payload"],
                "razorpay_abuse_takedown": remediation_res["takedown_payload"],
                "safety_playbook": remediation_res["safety_playbook"]
            },
            "agent_traces": all_traces
        }

    def stream_investigation(self, input_text: str) -> Generator[dict, None, None]:
        """
        Yields agent telemetry events in real-time for SSE (Server-Sent Events) streaming to UI.
        """
        context = {
            "input_text": input_text,
            "timestamp": time.time()
        }

        # Start Orchestration Event
        yield {
            "event": "ORCHESTRATOR_START",
            "message": "Swarm Orchestrator initialized. Dispatching 5 specialized forensic agents..."
        }

        # 1. OSINT Agent
        yield {"event": "AGENT_START", "agent": self.osint_agent.name, "icon": self.osint_agent.icon}
        osint_res = self.osint_agent.run(input_text, context)
        for log in self.osint_agent.thought_log:
            yield {"event": "AGENT_LOG", **log}
        context["osint"] = osint_res
        yield {"event": "AGENT_COMPLETE", "agent": self.osint_agent.name, "result": osint_res}

        # 2. Live Web Agent
        yield {"event": "AGENT_START", "agent": self.web_agent.name, "icon": self.web_agent.icon}
        web_res = self.web_agent.run(input_text, context)
        for log in self.web_agent.thought_log:
            yield {"event": "AGENT_LOG", **log}
        context["web"] = web_res
        yield {"event": "AGENT_COMPLETE", "agent": self.web_agent.name, "result": web_res}

        # 3. Cognitive Agent
        yield {"event": "AGENT_START", "agent": self.cognitive_agent.name, "icon": self.cognitive_agent.icon}
        cognitive_res = self.cognitive_agent.run(input_text, context)
        for log in self.cognitive_agent.thought_log:
            yield {"event": "AGENT_LOG", **log}
        context["cognitive"] = cognitive_res
        yield {"event": "AGENT_COMPLETE", "agent": self.cognitive_agent.name, "result": cognitive_res}

        # 4. Fintech Agent
        yield {"event": "AGENT_START", "agent": self.fintech_agent.name, "icon": self.fintech_agent.icon}
        fintech_res = self.fintech_agent.run(input_text, context)
        for log in self.fintech_agent.thought_log:
            yield {"event": "AGENT_LOG", **log}
        context["fintech"] = fintech_res
        yield {"event": "AGENT_COMPLETE", "agent": self.fintech_agent.name, "result": fintech_res}

        # 5. Arbitration
        yield {"event": "ARBITRATION_START", "message": "Synthesizing cross-agent telemetry, live DOM probes, and computing risk consensus..."}
        arbitration = self._arbitrate_risk(context)
        context.update(arbitration)

        # 6. Remediation Agent
        yield {"event": "AGENT_START", "agent": self.remediation_agent.name, "icon": self.remediation_agent.icon}
        remediation_res = self.remediation_agent.run(input_text, context)
        for log in self.remediation_agent.thought_log:
            yield {"event": "AGENT_LOG", **log}
        context["remediation"] = remediation_res
        yield {"event": "AGENT_COMPLETE", "agent": self.remediation_agent.name, "result": remediation_res}

        # Final Payload
        final_payload = {
            "overall_risk": context["overall_risk"],
            "risk_badge": context["risk_badge"],
            "confidence_score": context["confidence_score"],
            "analysis": context["analysis"],
            "recommendation": context["recommendation"],
            "vectors": {
                "osint_risk": osint_res.get("osint_risk_score", 0),
                "web_risk": web_res.get("web_risk_score", 0),
                "fintech_risk": fintech_res.get("fintech_risk_score", 0),
                "cognitive_risk": cognitive_res.get("cognitive_risk_score", 0)
            },
            "autonomous_actions": {
                "cybercrime_complaint": remediation_res["complaint_payload"],
                "razorpay_abuse_takedown": remediation_res["takedown_payload"],
                "safety_playbook": remediation_res["safety_playbook"]
            }
        }
        yield {"event": "FINAL_RESULT", "data": final_payload}

    def _arbitrate_risk(self, context: dict) -> dict:
        """
        Consensus engine calculating composite risk and combining agent insights.
        """
        osint_score = context["osint"].get("osint_risk_score", 0)
        web_score = context.get("web", {}).get("web_risk_score", 0)
        fintech_score = context["fintech"].get("fintech_risk_score", 0)
        cognitive_score = context["cognitive"].get("cognitive_risk_score", 0)

        # Check if all links in the payload are verified official enterprise endpoints
        has_domains = bool(context["osint"].get("domains_analyzed"))
        all_domains_official = (
            has_domains and
            all(any(t.get("status") == "LEGITIMATE_OFFICIAL" for t in d.get("typosquat", []))
                for d in context["osint"]["domains_analyzed"]) and
            osint_score == 0
        )

        # Check if any probed URL returned 404 or connection error
        has_dead_link = any(p.get("is_404_or_dead") for p in context.get("web", {}).get("probed_results", []))

        # Weighted composite score with non-linear boost for critical vectors
        if all_domains_official and not context["fintech"].get("is_payment_scam") and not has_dead_link:
            composite = 0
        elif context["osint"].get("is_spoofed_brand") or context["fintech"].get("is_payment_scam") or web_score >= 80:
            composite = max((osint_score * 0.30) + (web_score * 0.25) + (fintech_score * 0.25) + (cognitive_score * 0.20), 85)
        elif has_dead_link:
            composite = max(web_score, 45)
        else:
            composite = (osint_score * 0.30) + (web_score * 0.25) + (fintech_score * 0.25) + (cognitive_score * 0.20)

        composite_score = min(int(composite), 100)

        if composite_score >= 80:
            risk = "Critical Scam / Phishing"
            badge = "CRITICAL"
            recommendation = "🚨 IMMEDIATE THREAT: Do not interact, click links, or authenticate payments. File a complaint using the auto-generated cybercrime dossier."
        elif composite_score >= 50:
            risk = "High Risk"
            badge = "HIGH"
            recommendation = "⚠️ HIGH RISK: Multiple fraudulent indicators detected. Verify strictly through official authenticated enterprise portals."
        elif composite_score >= 25:
            risk = "Medium–Suspicious"
            badge = "MEDIUM"
            recommendation = "🔍 CAUTION: Anomalous patterns found. Proceed with heightened scrutiny."
        else:
            risk = "Verified Safe / Legitimate"
            badge = "SAFE"
            recommendation = "✅ VERIFIED AUTHENTIC: No scam signals, phishing domains, or fraudulent payment mechanics detected."

        # Aggregate explanation cards across agents
        combined_analysis = (
            context["osint"].get("explanations", []) +
            context.get("web", {}).get("explanations", []) +
            context["fintech"].get("explanations", []) +
            context["cognitive"].get("explanations", [])
        )

        if composite_score < 25:
            # If safe, provide positive verification evidence cards
            positive_cards = [
                {
                    "title": "✅ Verified Transactional Integrity",
                    "text": "Payload follows standard authentic business communication patterns with zero artificial urgency or coercive threats."
                },
                {
                    "title": "✅ Secure Payment Profile",
                    "text": "No deceptive UPI collect traps, suspicious VPA impersonations, or reverse debit mechanisms identified."
                },
                {
                    "title": "✅ Clean Network Footprint",
                    "text": "No brand lookalikes, typosquatting domains, or high-risk TLDs detected in the payload."
                }
            ]
            # Keep any explicit official domain verification cards and add positive cards
            domain_verified = [c for c in combined_analysis if "Official" in c.get("title", "") or "Authentic" in c.get("title", "")]
            combined_analysis = domain_verified + [p for p in positive_cards if not any(p["title"] == d["title"] for d in domain_verified)]
        elif not combined_analysis:
            combined_analysis = [{
                "title": "Standard Communication Pattern",
                "text": "Payload does not exhibit known deception, phishing lures, or malicious payment handles."
            }]

        return {
            "overall_risk": risk,
            "risk_badge": badge,
            "confidence_score": composite_score,
            "analysis": combined_analysis,
            "recommendation": recommendation
        }

