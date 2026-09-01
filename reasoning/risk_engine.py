"""
Sentinel AI 2.0 - Reasoning & Risk Engine Adapter
Provides unified entrypoint into the Multi-Agent Swarm Orchestration system.
"""

from core.orchestrator import SwarmOrchestrator

_orchestrator = SwarmOrchestrator()

def analyze_risk(text: str) -> dict:
    """Invokes the multi-agent swarm to evaluate input text."""
    return _orchestrator.run_investigation(text)

def stream_risk(text: str):
    """Streams live telemetry from the multi-agent swarm."""
    return _orchestrator.stream_investigation(text)

