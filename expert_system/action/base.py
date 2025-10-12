from __future__ import annotations

import dataclasses
from typing import Dict, Any, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from expert_system.base import BaseExpertSystem


@dataclasses.dataclass
class Action:
    """Domain-independent action."""

    action_type: str
    parameters: Dict[str, Any] = dataclasses.field(default_factory=dict)

    def execute(self, context: BaseExpertSystem) -> Any:
        """Execute action in the given context."""
        return context.execute_action(self)


class ActionRegistry:
    """Registry for action handlers."""

    def __init__(self):
        self._handlers: Dict[str, Callable] = {}

    def register(self, action_type: str, handler: Callable) -> None:
        """Register an action handler."""
        self._handlers[action_type] = handler

    def get(self, action_type: str) -> Callable:
        """Get a handler by action type."""
        if action_type not in self._handlers:
            raise ValueError(f"Unknown action type: {action_type}")
        return self._handlers[action_type]

    def has(self, action_type: str) -> bool:
        """Check if handler exists."""
        return action_type in self._handlers
