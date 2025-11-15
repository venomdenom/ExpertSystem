import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

import yaml

from loaders.fact import FactSchema, FactType


class DataLoader:
    """Loads actual data values."""

    @staticmethod
    def load(
            filepath: Path,
            schema: Optional[FactSchema] = None
    ) -> Dict[str, Any]:
        """Load single data entry."""
        suffix = filepath.suffix.lower()

        loaders = {
            '.json': DataLoader.load_from_json,
            '.yaml': DataLoader.load_from_yaml,
            '.yml': DataLoader.load_from_yaml,
        }

        loader = loaders.get(suffix)
        if not loader:
            raise ValueError(f"Unsupported format for data: {suffix}")

        data = loader(filepath)

        # Validate and apply defaults if schema provided
        if schema:
            data = schema.apply_defaults(data)
            is_valid, errors = schema.validate_data(data)
            if not is_valid:
                raise ValueError(f"Data validation failed: {errors}")

        return data

    @staticmethod
    def load_batch(
            filepath: Path,
            schema: Optional[FactSchema] = None
    ) -> List[Dict[str, Any]]:
        """Load multiple data entries (e.g., from CSV)."""
        suffix = filepath.suffix.lower()

        if suffix == '.csv':
            return DataLoader.load_from_csv(filepath, schema)
        else:
            # Single entry
            return [DataLoader.load(filepath, schema)]

    @staticmethod
    def load_from_json(filepath: Path) -> Dict[str, Any]:
        """Load data from JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data  # Support both wrapped and unwrapped

    @staticmethod
    def load_from_yaml(filepath: Path) -> Dict[str, Any]:
        """Load data from YAML."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return data

    @staticmethod
    def load_from_csv(filepath: Path, schema: Optional[FactSchema] = None) -> \
            List[Dict[str, Any]]:
        """Load multiple data entries from CSV."""
        results = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Convert types based on schema
                data = {}
                for key, value in row.items():
                    if schema and key in schema.facts:
                        fact_def = schema.facts[key]
                        data[key] = DataLoader._convert_type(value,
                                                             fact_def.type)
                    else:
                        data[key] = DataLoader._auto_convert(value)

                # Apply defaults and validate
                if schema:
                    data = schema.apply_defaults(data)
                    is_valid, errors = schema.validate_data(data)
                    if not is_valid:
                        print(f"Warning: Row validation failed: {errors}")
                        continue

                results.append(data)

        return results

    @staticmethod
    def _convert_type(value: str, fact_type: FactType) -> Any:
        """Convert string value to appropriate type."""
        if not value or value.strip() == '':
            return None

        if fact_type == FactType.NUMBER:
            try:
                return float(value) if '.' in value else int(value)
            except ValueError:
                return None

        elif fact_type == FactType.BOOLEAN:
            return value.lower() in ('true', '1', 'yes', 'y')

        elif fact_type == FactType.STRING or fact_type == FactType.ENUM:
            return value.strip()

        return value

    @staticmethod
    def _auto_convert(value: str) -> Any:
        """Auto-detect and convert type."""
        if not value or value.strip() == '':
            return None

        # Try boolean
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'

        # Try number
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            pass

        # Return as string
        return value.strip()


class DataValidator:
    """Validates data against schema."""

    @staticmethod
    def validate_batch(
            data_list: List[Dict[str, Any]],
            schema: FactSchema
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate multiple data entries.

        Returns:
            (valid_data, invalid_data_with_errors)
        """
        valid = []
        invalid = []

        for data in data_list:
            is_valid, errors = schema.validate_data(data)
            if is_valid:
                valid.append(data)
            else:
                invalid.append({
                    'data': data,
                    'errors': errors
                })

        return valid, invalid
