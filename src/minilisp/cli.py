"""Command-line interface for executing scripts or launching REPL."""
from __future__ import annotations

import argparse
import sys
from minilisp import run_code
from minilisp.repl import start_repl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="minilisp-py interpreter CLI")
    parser.add_argument("file", nargs="?", help="Optional .lisp file to execute")
    args = parser.parse_args(argv)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
            res = run_code(content)
            if res is not None:
                print(res)
            return 0
        except Exception as err:
            print(f"Execution Error: {err}", file=sys.stderr)
            return 1

    start_repl()
    return 0


if __name__ == "__main__":
    sys.exit(main())
