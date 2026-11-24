"""Parser unit tests."""
import unittest
from minilisp.lexer import Lexer
from minilisp.parser import Parser, ParserError
from minilisp.ast_nodes import (
    NumberNode,
    StringNode,
    SymbolNode,
    ListNode,
)


class TestParser(unittest.TestCase):
    def test_parse_nested_lists(self):
        code = "(define (square x) (* x x))"
        tokens = Lexer(code).tokenize()
        parser = Parser(tokens)
        nodes = parser.parse()

        self.assertEqual(len(nodes), 1)
        root = nodes[0]
        self.assertIsInstance(root, ListNode)
        self.assertEqual(len(root.elements), 3)

        self.assertEqual(root.elements[0], SymbolNode("define"))
        self.assertIsInstance(root.elements[1], ListNode)
        self.assertEqual(root.elements[1].elements, [SymbolNode("square"), SymbolNode("x")])
        self.assertIsInstance(root.elements[2], ListNode)

    def test_unclosed_paren_raises_error(self):
        tokens = Lexer("(+ 1 2").tokenize()
        parser = Parser(tokens)
        with self.assertRaises(ParserError):
            parser.parse()


if __name__ == "__main__":
    unittest.main()
