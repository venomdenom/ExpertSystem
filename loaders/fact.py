import dataclasses
import json
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional

import yaml

from loaders.base import BaseLoader


class FactType(Enum):
    """Supported fact types."""
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    ENUM = "enum"
    DATE = "date"
    ARRAY = "array"


@dataclasses.dataclass
class FactDefinition:
    """Definition of a fact in the system."""
    name: str
    type: FactType
    description: str = ""
    required: bool = False
    default: Any = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    enum_values: Optional[List[str]] = None
    unit: Optional[str] = None

    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        """Validate a value against this fact definition.

        Returns:
            (is_valid, error_message)
        """
        # Check required
        if value is None:
            if self.required:
                return False, f"Fact '{self.name}' is required"
            return True, None

        # Type validation
        if self.type == FactType.NUMBER:
            if not isinstance(value, (int, float)):
                return False, f"Fact '{self.name}' must be a number"
            if self.min_value is not None and value < self.min_value:
                return False, f"Fact '{self.name}' must be >= {self.min_value}"
            if self.max_value is not None and value > self.max_value:
                return False, f"Fact '{self.name}' must be <= {self.max_value}"

        elif self.type == FactType.STRING:
            if not isinstance(value, str):
                return False, f"Fact '{self.name}' must be a string"

        elif self.type == FactType.BOOLEAN:
            if not isinstance(value, bool):
                return False, f"Fact '{self.name}' must be a boolean"

        elif self.type == FactType.ENUM:
            if value not in (self.enum_values or []):
                return False, (f"Fact '{self.name}' "
                               f"must be one of {self.enum_values}")

        return True, None


class FactSchema:
    """Schema defining all facts in the system."""

    def __init__(self):
        self.facts: Dict[str, FactDefinition] = {}
        self.metadata: Dict[str, Any] = {}

    def add_fact(self, fact_def: FactDefinition):
        """Add a fact definition."""
        self.facts[fact_def.name] = fact_def

    def get_fact(self, name: str) -> Optional[FactDefinition]:
        """Get fact definition by name."""
        return self.facts.get(name)

    def validate_data(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate data against schema.

        Returns:
            (is_valid, list_of_errors)
        """
        errors = []

        # Check all defined facts
        for fact_name, fact_def in self.facts.items():
            value = data.get(fact_name)
            is_valid, error = fact_def.validate(value)
            if not is_valid:
                errors.append(error)

        # Check for undefined facts
        for data_key in data.keys():
            if data_key not in self.facts:
                errors.append(f"Unknown fact: '{data_key}'")

        return len(errors) == 0, errors

    def apply_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values to data."""
        result = data.copy()

        for fact_name, fact_def in self.facts.items():
            if fact_name not in result and fact_def.default is not None:
                result[fact_name] = fact_def.default

        return result


class FactLoader(BaseLoader):
    """Loads fact schemas from configuration files."""

    @staticmethod
    def load(filepath: Path) -> FactSchema:
        """Auto-detect format and load fact schema."""
        suffix = filepath.suffix.lower()

        loaders = {
            '.json': FactLoader.load_from_json,
            '.yaml': FactLoader.load_from_yaml,
            '.yml': FactLoader.load_from_yaml,
        }

        loader = loaders.get(suffix)
        if not loader:
            raise ValueError(f"Unsupported format for fact schema: {suffix}")

        return loader(filepath)

    @staticmethod
    def load_from_json(filepath: Path) -> FactSchema:
        """Load fact schema from JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return FactLoader._parse_schema(data)

    @staticmethod
    def load_from_yaml(filepath: Path) -> FactSchema:
        """Load fact schema from YAML."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return FactLoader._parse_schema(data)

    @staticmethod
    def _parse_schema(data: Dict[str, Any]) -> FactSchema:
        """Parse schema from dictionary."""
        schema = FactSchema()
        schema.metadata = data.get('metadata', {})

        facts_data = data.get('facts', {})
        for fact_name, fact_info in facts_data.items():
            fact_def = FactDefinition(
                name=fact_name,
                type=FactType(fact_info.get('type', 'string')),
                description=fact_info.get('description', ''),
                required=fact_info.get('required', False),
                default=fact_info.get('default'),
                min_value=fact_info.get('min'),
                max_value=fact_info.get('max'),
                enum_values=fact_info.get('values'),
                unit=fact_info.get('unit')
            )
            schema.add_fact(fact_def)

        return schema
