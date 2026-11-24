"""Interactive Read-Eval-Print Loop for minilisp."""
from __future__ import annotations

import sys
from minilisp.builtins import create_global_environment
from minilisp import run_code


def start_repl() -> None:
    print("Welcome to minilisp-py REPL! Type (exit) or Ctrl-C/D to quit.\n")
    env = create_global_environment()

    while True:
        try:
            line = input("minilisp> ")
            if not line.strip():
                continue
            if line.strip() in ("(exit)", "exit", "quit"):
                print("Goodbye!")
                break
            result = run_code(line, env)
            if result is not None:
                print(f"=> {result!r}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception as err:
            print(f"Error: {err}", file=sys.stderr)
