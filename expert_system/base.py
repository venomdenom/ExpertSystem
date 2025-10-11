from abc import ABC, abstractmethod
from typing import Any

from expert_system.action.base import ActionRegistry, Action
from expert_system.condition.evaluators import ConditionRegistry
from expert_system.fact_base import FactBase
from expert_system.rule import Rule


class BaseExpertSystem(ABC):
    """Domain-independent expert system base class."""

    def __init__(self):
        self.fact_base = FactBase()
        self.rules: list[Rule] = []
        self.fired_rules: list[str] = []
        self.results: dict[str, Any] = {}

        # Registries for extensibility
        self.condition_registry = ConditionRegistry()
        self.action_registry = ActionRegistry()

        # Allow subclasses to register custom operators and actions
        self._setup_custom_evaluators()
        self._setup_custom_actions()

    @abstractmethod
    def _setup_custom_evaluators(self) -> None:
        """Override to register custom condition evaluators."""
        pass

    @abstractmethod
    def _setup_custom_actions(self) -> None:
        """Override to register custom action handlers."""
        pass

    def add_fact(self, name: str, value: Any) -> None:
        """Add or update a single fact."""
        self.fact_base.set(name, value)

    def add_facts(self, facts: dict[str, Any]) -> None:
        """Add or update multiple facts."""
        self.fact_base.update(facts)

    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the system."""
        self.rules.append(rule)

    def add_rules(self, rules: list[Rule]) -> None:
        """Add multiple rules."""
        self.rules.extend(rules)

    def run_evaluation(self) -> None:
        """Execute the inference engine."""
        sorted_rules = sorted(self.rules, key=lambda r: r.priority,
                              reverse=True)

        for rule in sorted_rules:
            if rule.check(self.fact_base, self.condition_registry):
                self.fired_rules.append(rule.name)
                rule.execute(self)

    def execute_action(self, action: Action) -> Any:
        """Execute an action using the registered handler."""
        handler = self.action_registry.get(action.action_type)
        return handler(self, **action.parameters)

    def reset(self) -> None:
        """Reset the system state."""
        self.fact_base.clear()
        self.fired_rules.clear()
        self.results.clear()

    def get_results(self) -> dict[str, Any]:
        """Get evaluation results."""
        return self.results.copy()

    def get_facts(self) -> dict[str, Any]:
        """Get all facts."""
        return self.fact_base.all()
