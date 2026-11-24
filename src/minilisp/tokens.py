"""Token definitions for minilisp."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    NUMBER = auto()
    STRING = auto()
    SYMBOL = auto()
    BOOLEAN = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"
