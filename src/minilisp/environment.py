"""Lexical scoping and runtime environment."""
from __future__ import annotations

from typing import Any, Dict, Optional


class Environment:
    def __init__(self, parent: Optional[Environment] = None, bindings: Optional[Dict[str, Any]] = None) -> None:
        self.parent = parent
        self.bindings: Dict[str, Any] = dict(bindings or {})

    def get(self, name: str) -> Any:
        if name in self.bindings:
            return self.bindings[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise NameError(f"Symbol '{name}' is not bound in current environment.")

    def define(self, name: str, value: Any) -> None:
        self.bindings[name] = value

    def set(self, name: str, value: Any) -> None:
        if name in self.bindings:
            self.bindings[name] = value
            return
        if self.parent is not None:
            self.parent.set(name, value)
            return
        raise NameError(f"Cannot mutate unbound symbol '{name}'.")

    def extend(self, bindings: Dict[str, Any]) -> Environment:
        return Environment(parent=self, bindings=bindings)
