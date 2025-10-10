from abc import ABC
from typing import Any

from expert_system.models import Rule


class BaseExpertSystem(ABC):
    """Base class for all expert systems."""

    def __init__(self):
        self.facts = {}
        self.rules = []
        self.fired_rules = []
        self.results = {}

    def add_fact(self, name: str, value: Any):
        """Adds fact into the expert system."""
        if name not in self.facts:
            self.facts[name] = value

    def add_rule(self, rule: Rule):
        """Adds rule into the expert system."""
        self.rules.append(rule)

    def run_evaluation(self):
        """Runs thew expert system."""
        sorted_rules = sorted(
            self.rules,
            key=lambda r: r.priority,
            reverse=True
        )

        for rule in sorted_rules:
            if rule.check(self.facts):
                self.fired_rules.append(rule.name)
                rule.execute(self)

    def reset(self):
        """Resets the expert system state."""
        self.facts = {}
        self.fired_rules = []
        self.results = {}
