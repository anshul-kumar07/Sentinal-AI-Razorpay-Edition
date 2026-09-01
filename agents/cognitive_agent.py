"""
Sentinel AI 2.0 - Social Engineering & Cognitive Reasoning Agent
Dissects psychological pressure, artificial urgency, authority coercion, and manipulative linguistic patterns.
"""

from agents.base_agent import BaseAgent
from core.config import URGENCY_TRIGGERS, FINANCIAL_LURES, AUTHORITY_IMPERSONATIONS

class CognitiveAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Cognitive & Social Engineering Agent",
            role="Psychological Lures, Panic Index & Manipulation Forensics",
            icon="🧠"
        )

    def run(self, input_text: str, context: dict) -> dict:
        self.reset()
        self.status = "RUNNING"
        self.log("THOUGHT", "Initiating cognitive linguistic analysis to evaluate psychological manipulation and social engineering vectors...")

        text_lower = input_text.lower()
        cognitive_score = 0
        explanations = []
        detected_vectors = []

        # 1. Urgency / Panic Index Evaluation
        matched_urgency = [u for u in URGENCY_TRIGGERS if u in text_lower]
        if matched_urgency:
            self.log("TOOL_CALL", f"Evaluated urgency vectors -> Matched: {matched_urgency}")
            cognitive_score += 25
            detected_vectors.append("ARTIFICIAL_URGENCY")
            explanations.append({
                "title": "Artificial Urgency & Panic Coercion",
                "text": f"Payload uses high-pressure phrases ('{', '.join(matched_urgency[:3])}') to bypass critical thinking and force impulsive compliance."
            })

        # 2. Authority Impersonation Vectors
        matched_authority = [a for a in AUTHORITY_IMPERSONATIONS if a in text_lower]
        if matched_authority:
            self.log("TOOL_CALL", f"Evaluated authority vectors -> Matched: {matched_authority}")
            cognitive_score += 25
            detected_vectors.append("AUTHORITY_IMPERSONATION")
            explanations.append({
                "title": "Authority & Institutional Leverage",
                "text": f"Claims association with institutional authorities ('{', '.join(matched_authority)}') to induce compliance via fear or obedience."
            })

        # 3. Financial Lure & Unrealistic Incentive Vectors
        matched_lures = [f for f in FINANCIAL_LURES if f in text_lower]
        if matched_lures:
            self.log("TOOL_CALL", f"Evaluated financial lure vectors -> Matched: {matched_lures}")
            cognitive_score += 25
            detected_vectors.append("FINANCIAL_LURE")
            explanations.append({
                "title": "Unrealistic Financial Incentive / Task Bait",
                "text": f"Payload employs classic financial traps ('{', '.join(matched_lures[:2])}') promising effortless returns or unearned refunds."
            })

        # 4. Identity & Channel Integrity
        has_generic_greeting = any(g in text_lower for g in ["dear user", "dear customer", "dear candidate", "hello sir/madam"])
        if has_generic_greeting and (matched_urgency or matched_lures):
            cognitive_score += 15
            self.log("OBSERVATION", "Generic mass-broadcast salutation detected without personalized customer metadata.")
            explanations.append({
                "title": "Impersonal Mass Phishing Vector",
                "text": "Uses generic impersonal greetings typical of automated mass-phishing distribution."
            })

        self.log("DECISION", f"Cognitive Agent completed analysis. Psychological Manipulation Score: {cognitive_score}/100.")
        self.status = "COMPLETED"

        return {
            "cognitive_risk_score": min(cognitive_score, 100),
            "detected_vectors": detected_vectors,
            "explanations": explanations
        }

