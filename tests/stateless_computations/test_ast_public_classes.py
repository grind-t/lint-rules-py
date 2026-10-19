import ast

from lint_rules._stateless_computations.ast_public_classes import ast_public_classes


def test_public_classes(subtests):
    cases = [
        ("class A: ...\nclass B: ...", ["A", "B"]),
        ("class A: ...\nclass _B: ...", ["A"]),
        ("class A: ...\nclass E(Exception): ...", ["A"]),
        ("class A: ...\nclass E(LibError): ...", ["A"]),
        ("class A: ...\nclass E(ValueError): ...\nclass F(E): ...", ["A"]),
        ("from enum import Enum\nclass A: ...\nclass K(Enum): ...", ["A"]),
        ("import enum\nclass A: ...\nclass K(enum.StrEnum): ...", ["A"]),
        ("class A:\n    class Inner: ...", ["A"]),
        ("def f() -> None:\n    class Local: ...", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert ast_public_classes(ast.parse(source)) == expected
