from typing import Any


class FactBase:
    """Generic fact storage that works with any domain."""

    def __init__(self):
        self._facts: dict[str, Any] = {}

    def set(
            self,
            name: str,
            value: Any,
            overwrite: bool = True
    ):
        """Set the fact."""
        if not self._facts.get(name) or overwrite:
            self._facts[name] = value

    def get(self, name: str, fallback: Any = None) -> Any:
        """Get the fact."""
        return self._facts.get(name, fallback)

    def has(self, name):
        """Check if a fact exists."""
        return name in self._facts

    def update(self, facts: dict[str, Any]) -> None:
        """Update multiple facts at once."""
        self._facts.update(facts)

    def clear(self) -> None:
        """Clear all facts."""
        self._facts.clear()

    def all(self) -> dict[str, Any]:
        """Get all facts."""
        return self._facts.copy()
