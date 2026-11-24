# minilisp-py

A lightweight, clean, and robust Lisp/Scheme-like AST interpreter written in Python.

Built for compiler enthusiasts and designed for static code analysis, architectural call-graph generation, and AST evaluation benchmarking.

## Features

- **Lexer & Tokenizer:** Handles parentheses, string literals, integer/float numerals, comments (`;`), and symbol identifiers.
- **Recursive Descent Parser:** Transforms flat token streams into nested Abstract Syntax Tree (AST) nodes (`NumberNode`, `StringNode`, `SymbolNode`, `ListNode`).
- **Lexical Scoping & Environments:** Supports nested closures, lexically-scoped environments, and symbol bindings (`define`, `set!`, `let`).
- **Tree-Walking Evaluator:** Evaluates AST expressions with tail-call awareness and first-class functions / lambdas (`lambda`, `if`, `begin`, `quote`).
- **Standard Library:** Built-in arithmetic operators (`+`, `-`, `*`, `/`, `mod`), comparison predicates (`=`, `<`, `>`, `<=`, `>=`), and list primitives (`cons`, `car`, `cdr`, `list`, `null?`, `length`).
- **Interactive REPL & CLI Runner:** File execution and live interactive terminal REPL.

## Project Architecture

```text
minilisp-py/
├── src/
│   └── minilisp/
│       ├── __init__.py      # Package exports and convenience evaluate()
│       ├── tokens.py        # Token definitions and TokenType enum
│       ├── lexer.py         # Lexical analyzer / tokenizer
│       ├── ast_nodes.py     # AST node hierarchy (ASTNode, NumberNode, etc.)
│       ├── parser.py        # S-expression parser
│       ├── environment.py   # Lexical scope and symbol environment
│       ├── builtins.py      # Core primitive library and functions
│       ├── evaluator.py     # Tree-walking AST evaluator
│       ├── repl.py          # Interactive REPL interface
│       └── cli.py           # Command-line entry point
└── tests/
    ├── __init__.py
    ├── test_lexer.py        # Tokenizer unit tests
    ├── test_parser.py       # S-expression AST parser tests
    └── test_evaluator.py    # Runtime execution and lambda/recursion tests
```

## Running Tests

Run the test suite using Python's standard `unittest`:

```bash
python3 -m unittest discover tests
```

## Running the REPL

```bash
python3 -m minilisp.cli
```

Or execute a script directly:

```bash
python3 -m minilisp.cli path/to/script.lisp
```
