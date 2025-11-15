import csv
import json
from pathlib import Path
from typing import List, Dict, Any

import yaml

from expert_system.action.base import Action
from expert_system.condition.base import Condition
from expert_system.rule import Rule
from loaders.base import BaseLoader


class RuleLoader(BaseLoader):
    """Universal rule loader supporting multiple formats."""

    @staticmethod
    def load(filepath: Path) -> List[Rule]:
        """Auto-detect format and load rules."""
        suffix = filepath.suffix.lower()

        loaders = {
            '.json': RuleLoader.load_from_json,
            '.yaml': RuleLoader.load_from_yaml,
            '.yml': RuleLoader.load_from_yaml,
            '.csv': RuleLoader.load_from_csv,
        }

        loader = loaders.get(suffix)
        if not loader:
            raise ValueError(f"Unsupported file format: {suffix}")

        return loader(filepath)

    @staticmethod
    def load_from_json(filepath: Path) -> List[Rule]:
        """Load rules from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return RuleLoader._parse_rules(data.get('rules', []))

    @staticmethod
    def load_from_yaml(filepath: Path) -> List[Rule]:
        """Load rules from YAML file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return RuleLoader._parse_rules(data.get('rules', []))

    @staticmethod
    def load_from_csv(filepath: Path) -> List[Rule]:
        """Load simple rules from CSV file.

        Expected columns:
        - name, priority, fact, operator, value, action_type, 
          probability, status, recommendation
        """
        rules_data = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                rule = {
                    'name': row['name'],
                    'priority': int(row.get('priority', 0)),
                    'conditions': [{
                        'fact': row['fact'],
                        'operator': row['operator'],
                        'value': RuleLoader._parse_value(row['value'])
                    }],
                    'actions': [{
                        'type': row['action_type'],
                        'parameters': {
                            'probability': int(row.get('probability', 0)),
                            'status': row.get('status', ''),
                            'recommendation': row.get('recommendation', '')
                        }
                    }]
                }
                rules_data.append(rule)

        return RuleLoader._parse_rules(rules_data)

    @staticmethod
    def _parse_rules(rules_data: List[Dict[str, Any]]) -> List[Rule]:
        """Parse rules from dictionary format."""
        rules = []

        for rule_data in rules_data:
            conditions = [
                Condition(
                    fact_name=c['fact'],
                    operator=c['operator'],
                    value=c['value']
                )
                for c in rule_data.get('conditions', [])
            ]

            actions = [
                Action(
                    action_type=a['type'],
                    parameters=a.get('parameters', {})
                )
                for a in rule_data.get('actions', [])
            ]

            rules.append(Rule(
                name=rule_data['name'],
                conditions=conditions,
                actions=actions,
                priority=rule_data.get('priority', 0),
                description=rule_data.get('description', '')
            ))

        return rules

    @staticmethod
    def _parse_value(value_str: str) -> Any:
        """Parse string value to appropriate type."""
        # Try to parse as number
        try:
            if '.' in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            pass

        # Check for boolean
        if value_str.lower() in ('true', 'false'):
            return value_str.lower() == 'true'

        # Return as string
        return value_str


class ConfigValidator:
    """Validates configuration files."""

    @staticmethod
    def validate_json_schema(filepath: Path) -> bool:
        """Validate JSON config against schema."""
        schema = {
            "type": "object",
            "properties": {
                "metadata": {"type": "object"},
                "rules": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "conditions", "actions"],
                        "properties": {
                            "name": {"type": "string"},
                            "priority": {"type": "integer"},
                            "conditions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["fact", "operator", "value"]
                                }
                            },
                            "actions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["type"]
                                }
                            }
                        }
                    }
                }
            },
            "required": ["rules"]
        }

        try:
            import jsonschema
            with open(filepath) as f:
                data = json.load(f)
            jsonschema.validate(data, schema)
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
