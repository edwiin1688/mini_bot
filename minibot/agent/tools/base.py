"""Base tool class."""

from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """工具抽象基底類別，所有工具都必須繼承此類別。"""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def description(self) -> str: ...

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]: ...

    @abstractmethod
    async def execute(self, **kwargs) -> str: ...

    def to_schema(self) -> dict[str, Any]:
        """轉換為 LLM tool calling schema 格式。"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }
