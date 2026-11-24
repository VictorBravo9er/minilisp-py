"""Abstract Syntax Tree node representations for minilisp."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List


class ASTNode(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass


@dataclass(frozen=True)
class NumberNode(ASTNode):
    value: int | float

    def __repr__(self) -> str:
        return f"Number({self.value})"


@dataclass(frozen=True)
class StringNode(ASTNode):
    value: str

    def __repr__(self) -> str:
        return f"String({self.value!r})"


@dataclass(frozen=True)
class BooleanNode(ASTNode):
    value: bool

    def __repr__(self) -> str:
        return f"Boolean({self.value})"


@dataclass(frozen=True)
class SymbolNode(ASTNode):
    name: str

    def __repr__(self) -> str:
        return f"Symbol({self.name})"


@dataclass(frozen=True)
class ListNode(ASTNode):
    elements: List[ASTNode]

    def __repr__(self) -> str:
        inner = ", ".join(repr(e) for e in self.elements)
        return f"List([{inner}])"
