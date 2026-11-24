"""Lexical analyzer transforming raw text into minilisp tokens."""
from __future__ import annotations

from typing import List
from minilisp.tokens import Token, TokenType


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"LexerError at line {line}, col {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(source)

    def _peek(self) -> str | None:
        if self.pos < self.length:
            return self.source[self.pos]
        return None

    def _advance(self) -> str | None:
        ch = self._peek()
        if ch is not None:
            self.pos += 1
            if ch == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < self.length:
            ch = self._peek()

            # Skip whitespace
            if ch in (" ", "\t", "\r", "\n"):
                self._advance()
                continue

            # Skip line comments starting with ;
            if ch == ";":
                while self._peek() not in (None, "\n"):
                    self._advance()
                continue

            start_line = self.line
            start_col = self.column

            if ch == "(":
                self._advance()
                tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col))
            elif ch == ")":
                self._advance()
                tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col))
            elif ch == '"':
                tokens.append(self._read_string(start_line, start_col))
            elif ch in ("+", "-") and self._is_digit_ahead():
                tokens.append(self._read_number(start_line, start_col))
            elif ch.isdigit():
                tokens.append(self._read_number(start_line, start_col))
            elif ch == "#":
                tokens.append(self._read_boolean(start_line, start_col))
            elif self._is_symbol_char(ch):
                tokens.append(self._read_symbol(start_line, start_col))
            else:
                raise LexerError(f"Unexpected character: {ch!r}", start_line, start_col)

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens

    def _is_digit_ahead(self) -> bool:
        if self.pos + 1 < self.length:
            return self.source[self.pos + 1].isdigit()
        return False

    def _is_symbol_char(self, ch: str) -> bool:
        return (
            ch.isalnum()
            or ch in ("+", "-", "*", "/", "%", "<", ">", "=", "!", "?", "_", "$", "@", ":", ".")
        )

    def _read_string(self, start_line: int, start_col: int) -> Token:
        self._advance()  # consume opening quote
        chars: List[str] = []
        while True:
            ch = self._peek()
            if ch is None:
                raise LexerError("Unterminated string literal", start_line, start_col)
            if ch == '"':
                self._advance()
                break
            if ch == "\\":
                self._advance()
                esc = self._advance()
                if esc == "n":
                    chars.append("\n")
                elif esc == "t":
                    chars.append("\t")
                elif esc == '"':
                    chars.append('"')
                elif esc == "\\":
                    chars.append("\\")
                else:
                    chars.append(esc or "")
            else:
                chars.append(self._advance() or "")
        return Token(TokenType.STRING, "".join(chars), start_line, start_col)

    def _read_number(self, start_line: int, start_col: int) -> Token:
        chars: List[str] = []
        if self._peek() in ("+", "-"):
            chars.append(self._advance() or "")

        is_float = False
        while self.pos < self.length:
            ch = self._peek()
            if ch is not None and ch.isdigit():
                chars.append(self._advance() or "")
            elif ch == "." and not is_float:
                is_float = True
                chars.append(self._advance() or "")
            else:
                break

        num_str = "".join(chars)
        val = float(num_str) if is_float else int(num_str)
        return Token(TokenType.NUMBER, val, start_line, start_col)

    def _read_boolean(self, start_line: int, start_col: int) -> Token:
        self._advance()  # consume '#'
        ch = self._advance()
        if ch == "t":
            return Token(TokenType.BOOLEAN, True, start_line, start_col)
        elif ch == "f":
            return Token(TokenType.BOOLEAN, False, start_line, start_col)
        raise LexerError(f"Invalid boolean literal: #{ch}", start_line, start_col)

    def _read_symbol(self, start_line: int, start_col: int) -> Token:
        chars: List[str] = []
        while self.pos < self.length:
            ch = self._peek()
            if ch is not None and self._is_symbol_char(ch):
                chars.append(self._advance() or "")
            else:
                break
        return Token(TokenType.SYMBOL, "".join(chars), start_line, start_col)
