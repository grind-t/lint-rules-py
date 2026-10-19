import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_public_non_protocol_classes import (
    ast_public_non_protocol_classes,
)


def test_public_non_protocol_classes(subtests):
    cases = [
        ("class A: ...", [("A", SourceLocation(1, 1))]),
        ("class _A: ...", []),
        ("class P(Protocol): ...", []),
        ("class P(typing.Protocol[T]): ...", []),
        ("class E(ValueError): ...", [("E", SourceLocation(1, 1))]),
        ("def f():\n    class Local: ...", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert ast_public_non_protocol_classes(ast.parse(source)) == expected
