"""Lexer unit tests."""
import unittest
from minilisp.lexer import Lexer, LexerError
from minilisp.tokens import TokenType


class TestLexer(unittest.TestCase):
    def test_tokenize_primitives(self):
        code = '(+ 42 -12 3.14 "hello world" #t #f)'
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        types = [t.type for t in tokens]
        self.assertEqual(
            types,
            [
                TokenType.LPAREN,
                TokenType.SYMBOL,
                TokenType.NUMBER,
                TokenType.NUMBER,
                TokenType.NUMBER,
                TokenType.STRING,
                TokenType.BOOLEAN,
                TokenType.BOOLEAN,
                TokenType.RPAREN,
                TokenType.EOF,
            ],
        )
        self.assertEqual(tokens[2].value, 42)
        self.assertEqual(tokens[3].value, -12)
        self.assertAlmostEqual(tokens[4].value, 3.14)
        self.assertEqual(tokens[5].value, "hello world")
        self.assertEqual(tokens[6].value, True)
        self.assertEqual(tokens[7].value, False)

    def test_ignore_comments_and_whitespace(self):
        code = """
        ; Compute square
        (+ 5 ; inline comment
           5)
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        values = [t.value for t in tokens if t.type != TokenType.EOF]
        self.assertEqual(values, ["(", "+", 5, 5, ")"])

    def test_unterminated_string_error(self):
        lexer = Lexer('"unclosed string')
        with self.assertRaises(LexerError):
            lexer.tokenize()


if __name__ == "__main__":
    unittest.main()
