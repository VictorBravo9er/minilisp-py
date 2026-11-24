"""Evaluator unit tests covering arithmetic, closures, recursion, and builtins."""
import unittest
from minilisp import run_code


class TestEvaluator(unittest.TestCase):
    def test_arithmetic_eval(self):
        self.assertEqual(run_code("(+ 1 2 3 4)"), 10)
        self.assertEqual(run_code("(- 10 3 2)"), 5)
        self.assertEqual(run_code("(* 2 3 4)"), 24)
        self.assertEqual(run_code("(/ 10 2)"), 5.0)
        self.assertEqual(run_code("(mod 17 5)"), 2)

    def test_lexical_binding_and_closures(self):
        code = """
        (begin
            (define make-adder (lambda (x) (lambda (y) (+ x y))))
            (define add10 (make-adder 10))
            (add10 25))
        """
        self.assertEqual(run_code(code), 35)

    def test_recursive_fibonacci(self):
        code = """
        (begin
            (define (fib n)
                (if (<= n 1)
                    n
                    (+ (fib (- n 1)) (fib (- n 2)))))
            (fib 7))
        """
        self.assertEqual(run_code(code), 13)

    def test_list_primitives(self):
        self.assertEqual(run_code("(cons 1 (list 2 3))"), [1, 2, 3])
        self.assertEqual(run_code("(car (list 10 20 30))"), 10)
        self.assertEqual(run_code("(cdr (list 10 20 30))"), [20, 30])
        self.assertEqual(run_code("(null? (list))"), True)
        self.assertEqual(run_code("(null? (list 1))"), False)
        self.assertEqual(run_code("(length (list 1 2 3 4 5))"), 5)


if __name__ == "__main__":
    unittest.main()
