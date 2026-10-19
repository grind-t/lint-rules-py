import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)


def test_public_functions(subtests):
    cases = [
        (
            "def f(): ...\nasync def g(): ...",
            [("f", SourceLocation(1, 1)), ("g", SourceLocation(2, 1))],
        ),
        ("def f(): ...\ndef _g(): ...", [("f", SourceLocation(1, 1))]),
        ("def f():\n    def inner(): ...", [("f", SourceLocation(1, 1))]),
        ("class A:\n    def method(self): ...", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert ast_public_functions(ast.parse(source)) == expected
