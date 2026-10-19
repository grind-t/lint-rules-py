import ast

from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)


def test_public_functions(subtests):
    cases = [
        ("def f(): ...\ndef g(): ...", ["f", "g"]),
        ("def f(): ...\nasync def g(): ...", ["f", "g"]),
        ("def f(): ...\ndef _g(): ...", ["f"]),
        ("def f():\n    def inner(): ...", ["f"]),
        ("class A:\n    def method(self): ...", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert ast_public_functions(ast.parse(source)) == expected
