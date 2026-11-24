"""Tree-walking AST evaluator for minilisp expressions."""
from __future__ import annotations

from typing import Any, Callable, List
from minilisp.ast_nodes import (
    ASTNode,
    NumberNode,
    StringNode,
    BooleanNode,
    SymbolNode,
    ListNode,
)
from minilisp.environment import Environment


class Lambda:
    def __init__(self, params: List[str], body: List[ASTNode], env: Environment) -> None:
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args: Any) -> Any:
        if len(args) != len(self.params):
            raise TypeError(f"Lambda expected {len(self.params)} arguments, got {len(args)}")
        call_env = self.env.extend(dict(zip(self.params, args)))
        result = None
        for expr in self.body:
            result = evaluate(expr, call_env)
        return result


def evaluate(node: ASTNode, env: Environment) -> Any:
    if isinstance(node, NumberNode):
        return node.value
    if isinstance(node, StringNode):
        return node.value
    if isinstance(node, BooleanNode):
        return node.value
    if isinstance(node, SymbolNode):
        return env.get(node.name)

    if isinstance(node, ListNode):
        if len(node.elements) == 0:
            return []

        head = node.elements[0]

        # Special Form: (define <symbol> <expr>)
        if isinstance(head, SymbolNode) and head.name == "define":
            if len(node.elements) < 3:
                raise SyntaxError("Malformed define syntax: (define <name> <val>)")
            target = node.elements[1]
            if isinstance(target, SymbolNode):
                val = evaluate(node.elements[2], env)
                env.define(target.name, val)
                return val
            elif isinstance(target, ListNode) and len(target.elements) > 0:
                # Shortcut syntax: (define (foo x y) body)
                name_sym = target.elements[0]
                if not isinstance(name_sym, SymbolNode):
                    raise SyntaxError("Function name must be a symbol")
                param_names = [p.name for p in target.elements[1:] if isinstance(p, SymbolNode)]
                func = Lambda(param_names, node.elements[2:], env)
                env.define(name_sym.name, func)
                return func
            else:
                raise SyntaxError("Invalid define target")

        # Special Form: (set! <symbol> <expr>)
        if isinstance(head, SymbolNode) and head.name == "set!":
            target = node.elements[1]
            if not isinstance(target, SymbolNode):
                raise SyntaxError("set! variable must be a symbol")
            val = evaluate(node.elements[2], env)
            env.set(target.name, val)
            return val

        # Special Form: (lambda (<params...>) <body...>)
        if isinstance(head, SymbolNode) and head.name == "lambda":
            params_node = node.elements[1]
            if not isinstance(params_node, ListNode):
                raise SyntaxError("lambda parameter list must be a list")
            params = [p.name for p in params_node.elements if isinstance(p, SymbolNode)]
            body = node.elements[2:]
            return Lambda(params, body, env)

        # Special Form: (if <cond> <then> [else])
        if isinstance(head, SymbolNode) and head.name == "if":
            cond_val = evaluate(node.elements[1], env)
            if cond_val not in (False, None):
                return evaluate(node.elements[2], env)
            elif len(node.elements) > 3:
                return evaluate(node.elements[3], env)
            return None

        # Special Form: (begin <expr1> <expr2> ...)
        if isinstance(head, SymbolNode) and head.name == "begin":
            result = None
            for expr in node.elements[1:]:
                result = evaluate(expr, env)
            return result

        # Special Form: (quote <expr>)
        if isinstance(head, SymbolNode) and head.name == "quote":
            return _ast_to_raw(node.elements[1])

        # Normal Function / Operator Application
        fn = evaluate(head, env)
        if not callable(fn):
            raise TypeError(f"'{head}' evaluated to non-callable object {fn!r}")

        args = [evaluate(elem, env) for elem in node.elements[1:]]
        return fn(*args)

    raise ValueError(f"Unknown AST node type: {node!r}")


def _ast_to_raw(node: ASTNode) -> Any:
    if isinstance(node, (NumberNode, StringNode, BooleanNode)):
        return node.value
    if isinstance(node, SymbolNode):
        return node.name
    if isinstance(node, ListNode):
        return [_ast_to_raw(e) for e in node.elements]
    return node
