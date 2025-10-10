import dataclasses
from typing import List, Callable, Any


@dataclasses.dataclass
class Rule:
    """Class for rule representation."""

    name: str
    conditions: List[Callable]
    actions: List[Callable]
    priority: int = 0

    def check(self, facts: Any) -> bool:
        """Checks whether all the conditions are satisfied."""
        for condition in self.conditions:
            if not condition(facts):
                return False

        return True

    def execute(self, context) -> List[Any]:
        """Runs all the actions."""
        return [action(context) for action in self.actions]
