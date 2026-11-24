"""Builtin functions and standard library for minilisp."""
from __future__ import annotations

import operator
from functools import reduce
from typing import Any, Callable, Dict, List
from minilisp.environment import Environment


def _add(*args: Any) -> Any:
    return sum(args)


def _sub(*args: Any) -> Any:
    if len(args) == 0:
        raise TypeError("- requires at least 1 argument")
    if len(args) == 1:
        return -args[0]
    return reduce(operator.sub, args)


def _mul(*args: Any) -> Any:
    return reduce(operator.mul, args, 1)


def _div(*args: Any) -> Any:
    if len(args) == 0:
        raise TypeError("/ requires at least 1 argument")
    if len(args) == 1:
        return 1 / args[0]
    return reduce(operator.truediv, args)


def _mod(a: Any, b: Any) -> Any:
    return a % b


def _eq(*args: Any) -> bool:
    if len(args) < 2:
        return True
    return all(args[i] == args[i + 1] for i in range(len(args) - 1))


def _lt(*args: Any) -> bool:
    return all(args[i] < args[i + 1] for i in range(len(args) - 1))


def _gt(*args: Any) -> bool:
    return all(args[i] > args[i + 1] for i in range(len(args) - 1))


def _lte(*args: Any) -> bool:
    return all(args[i] <= args[i + 1] for i in range(len(args) - 1))


def _gte(*args: Any) -> bool:
    return all(args[i] >= args[i + 1] for i in range(len(args) - 1))


def _cons(car: Any, cdr: Any) -> List[Any]:
    if isinstance(cdr, list):
        return [car] + cdr
    return [car, cdr]


def _car(lst: List[Any]) -> Any:
    if not isinstance(lst, list) or len(lst) == 0:
        raise TypeError("car requires a non-empty list")
    return lst[0]


def _cdr(lst: List[Any]) -> List[Any]:
    if not isinstance(lst, list) or len(lst) == 0:
        raise TypeError("cdr requires a non-empty list")
    return lst[1:]


def _is_null(lst: Any) -> bool:
    return isinstance(lst, list) and len(lst) == 0


def _list_len(lst: List[Any]) -> int:
    if not isinstance(lst, list):
        raise TypeError("length requires a list")
    return len(lst)


def create_global_environment() -> Environment:
    env = Environment()
    builtins: Dict[str, Callable[..., Any]] = {
        "+": _add,
        "-": _sub,
        "*": _mul,
        "/": _div,
        "mod": _mod,
        "=": _eq,
        "<": _lt,
        ">": _gt,
        "<=": _lte,
        ">=": _gte,
        "cons": _cons,
        "car": _car,
        "cdr": _cdr,
        "list": lambda *args: list(args),
        "null?": _is_null,
        "length": _list_len,
        "not": operator.not_,
        "print": lambda *args: print(*args) or None,
    }
    for name, func in builtins.items():
        env.define(name, func)
    return env
