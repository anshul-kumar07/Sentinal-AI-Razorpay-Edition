"""
Sentinel AI 2.0 - Abstract Base Agent
Provides foundational execution lifecycle, thought tracing, tool telemetry, and structured reporting.
"""

from abc import ABC, abstractmethod
import datetime
from typing import Any

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, icon: str = "🤖"):
        self.name = name
        self.role = role
        self.icon = icon
        self.thought_log: list[dict] = []
        self.status = "IDLE"

    def log(self, step_type: str, message: str, data: Any = None) -> dict:
        """
        Records an agentic action, thought, tool execution, or observation into the live telemetry trace.
        """
        entry = {
            "agent": self.name,
            "role": self.role,
            "icon": self.icon,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "type": step_type,  # 'THOUGHT', 'TOOL_CALL', 'OBSERVATION', 'DECISION', 'WARNING'
            "message": message,
            "data": data
        }
        self.thought_log.append(entry)
        return entry

    def reset(self):
        """Resets the agent's thought log for a new investigation cycle."""
        self.thought_log = []
        self.status = "IDLE"

    @abstractmethod
    def run(self, input_text: str, context: dict) -> dict:
        """
        Executes the agent's autonomous workflow.
        Returns structured findings to be merged into the blackboard context.
        """
        pass

