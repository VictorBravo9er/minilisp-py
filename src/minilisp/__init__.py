"""Convenience public API for minilisp."""
from __future__ import annotations

from typing import Any
from minilisp.lexer import Lexer
from minilisp.parser import Parser
from minilisp.environment import Environment
from minilisp.builtins import create_global_environment
from minilisp.evaluator import evaluate

__all__ = [
    "Lexer",
    "Parser",
    "Environment",
    "create_global_environment",
    "evaluate",
    "run_code",
]


def run_code(source: str, env: Environment | None = None) -> Any:
    if env is None:
        env = create_global_environment()
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    nodes = parser.parse()
    last_res = None
    for node in nodes:
        last_res = evaluate(node, env)
    return last_res
