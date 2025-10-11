from abc import ABC, abstractmethod
from typing import Any


class BaseLoader(ABC):

    @abstractmethod
    def load(
            self,
            *args,
            **kwargs
    ) -> Any:
        raise NotImplementedError("Must be implemented by subclass")
