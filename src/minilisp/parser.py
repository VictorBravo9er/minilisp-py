"""Recursive descent parser generating minilisp AST from tokens."""
from __future__ import annotations

from typing import List
from minilisp.tokens import Token, TokenType
from minilisp.ast_nodes import (
    ASTNode,
    NumberNode,
    StringNode,
    BooleanNode,
    SymbolNode,
    ListNode,
)


class ParserError(Exception):
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(f"ParserError at line {token.line}, col {token.column}: {message}")
        self.token = token


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        tok = self._peek()
        if tok.type != TokenType.EOF:
            self.pos += 1
        return tok

    def parse(self) -> List[ASTNode]:
        expressions: List[ASTNode] = []
        while self._peek().type != TokenType.EOF:
            expressions.append(self.parse_expression())
        return expressions

    def parse_expression(self) -> ASTNode:
        tok = self._peek()

        if tok.type == TokenType.LPAREN:
            return self._parse_list()
        elif tok.type == TokenType.RPAREN:
            raise ParserError("Unexpected closing parenthesis ')'", tok)
        elif tok.type == TokenType.NUMBER:
            self._advance()
            return NumberNode(tok.value)
        elif tok.type == TokenType.STRING:
            self._advance()
            return StringNode(tok.value)
        elif tok.type == TokenType.BOOLEAN:
            self._advance()
            return BooleanNode(tok.value)
        elif tok.type == TokenType.SYMBOL:
            self._advance()
            return SymbolNode(tok.value)
        elif tok.type == TokenType.EOF:
            raise ParserError("Unexpected end of file while parsing expression", tok)
        else:
            raise ParserError(f"Unexpected token {tok}", tok)

    def _parse_list(self) -> ListNode:
        lparen = self._advance()  # consume '('
        elements: List[ASTNode] = []

        while self._peek().type != TokenType.RPAREN:
            if self._peek().type == TokenType.EOF:
                raise ParserError("Unclosed parenthesis, reached EOF", lparen)
            elements.append(self.parse_expression())

        self._advance()  # consume ')'
        return ListNode(elements)
