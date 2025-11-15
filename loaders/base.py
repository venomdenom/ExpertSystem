from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any


class ConfigFormat(StrEnum):
    """Supported configuration formats."""
    JSON = "json"
    YAML = "yaml"
    CSV = "csv"


class BaseLoader(ABC):

    @abstractmethod
    def load(
            self,
            *args,
            **kwargs
    ) -> Any:
        raise NotImplementedError("Must be implemented by subclass")
