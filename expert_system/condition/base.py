import dataclasses
from typing import Any

from expert_system.condition.evaluators import ConditionRegistry
from expert_system.fact_base import FactBase


@dataclasses.dataclass
class Condition:
    """Domain-independent condition."""

    fact_name: str
    operator: str
    value: Any

    def evaluate(
            self,
            fact_base: FactBase,
            registry: ConditionRegistry
    ) -> bool:
        """Evaluate condition against fact base."""
        if not fact_base.has(self.fact_name):
            return False

        fact_value = fact_base.get(self.fact_name)
        evaluator = registry.get(self.operator)

        try:
            return evaluator(fact_value, self.value)
        except Exception as e:
            # Log error but don't crash the system
            print(
                f"Error evaluating condition "
                f"{self.fact_name} "
                f"{self.operator} "
                f"{self.value}: "
                f"{e}")
            return False
