from typing import Protocol, Any, Callable


class ConditionEvaluator(Protocol):
    """Protocol for condition evaluators."""

    def evaluate(self, fact_value: Any, expected_value: Any) -> bool:
        """Evaluate a condition."""
        ...


class NumericRangeEvaluator:
    """Evaluates numeric range conditions."""

    @staticmethod
    def between(fact_value: Any, expected_value: tuple) -> bool:
        """Check if value is between min and max."""
        min_val, max_val = expected_value
        return min_val <= fact_value < max_val

    @staticmethod
    def gte(fact_value: Any, expected_value: Any) -> bool:
        return fact_value >= expected_value

    @staticmethod
    def lte(fact_value: Any, expected_value: Any) -> bool:
        return fact_value <= expected_value

    @staticmethod
    def gt(fact_value: Any, expected_value: Any) -> bool:
        return fact_value > expected_value

    @staticmethod
    def lt(fact_value: Any, expected_value: Any) -> bool:
        return fact_value < expected_value


class LogicalEvaluator:
    """Evaluates logical conditions."""

    @staticmethod
    def eq(fact_value: Any, expected_value: Any) -> bool:
        return fact_value == expected_value

    @staticmethod
    def neq(fact_value: Any, expected_value: Any) -> bool:
        return fact_value != expected_value

    @staticmethod
    def in_list(fact_value: Any, expected_value: list) -> bool:
        return fact_value in expected_value

    @staticmethod
    def contains(fact_value: Any, expected_value: Any) -> bool:
        return expected_value in fact_value


class ConditionRegistry:
    """Registry for all available condition evaluators."""

    def __init__(self):
        self._evaluators: dict[str, Callable] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register default evaluators."""
        # Numeric
        self.register(
            NumericRangeEvaluator.gte.__name__, NumericRangeEvaluator.gte)
        self.register(
            NumericRangeEvaluator.lte.__name__, NumericRangeEvaluator.lte)
        self.register(
            NumericRangeEvaluator.gt.__name__, NumericRangeEvaluator.gt)
        self.register(
            NumericRangeEvaluator.lt.__name__, NumericRangeEvaluator.lt)
        self.register(
            NumericRangeEvaluator.between.__name__,
            NumericRangeEvaluator.between
        )

        # Logical
        self.register(LogicalEvaluator.eq.__name__, LogicalEvaluator.eq)
        self.register(LogicalEvaluator.eq.__name__, LogicalEvaluator.neq)
        self.register(
            'in', LogicalEvaluator.in_list)
        self.register(
            LogicalEvaluator.contains.__name__, LogicalEvaluator.contains)

    def register(self, name: str, evaluator: Callable) -> None:
        """Register a custom evaluator."""
        self._evaluators[name] = evaluator

    def get(self, name: str) -> Callable:
        """Get an evaluator by name."""
        if name not in self._evaluators:
            raise ValueError(f"Unknown operator: {name}")
        return self._evaluators[name]

    def has(self, name: str) -> bool:
        """Check if evaluator exists."""
        return name in self._evaluators
