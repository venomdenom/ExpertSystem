from __future__ import annotations

import dataclasses
from typing import Any, TYPE_CHECKING

from expert_system.action.base import Action
from expert_system.condition.base import Condition
from expert_system.condition.evaluators import ConditionRegistry
from expert_system.fact_base import FactBase


if TYPE_CHECKING:
    from expert_system.base import BaseExpertSystem


@dataclasses.dataclass
class Rule:
    """Domain-independent rule."""

    name: str
    conditions: list[Condition]
    actions: list[Action]
    priority: int = 0
    description: str = ""

    def check(self, fact_base: FactBase, registry: ConditionRegistry) -> bool:
        """Check if all conditions are satisfied."""
        return all(condition.evaluate(fact_base, registry) for condition in
                   self.conditions)

    def execute(self, context: BaseExpertSystem) -> list[Any]:
        """Execute all actions."""
        return [action.execute(context) for action in self.actions]
