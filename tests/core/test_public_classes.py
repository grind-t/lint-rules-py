import ast

import pytest

from lint_rules._core.public_classes import public_classes


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("class A: ...\nclass B: ...", ["A", "B"]),
        ("class A: ...\nclass _B: ...", ["A"]),
        ("class A: ...\nclass E(Exception): ...", ["A"]),
        ("class A: ...\nclass E(LibError): ...", ["A"]),
        ("class A: ...\nclass E(ValueError): ...\nclass F(E): ...", ["A"]),
        ("from enum import Enum\nclass A: ...\nclass K(Enum): ...", ["A"]),
        ("import enum\nclass A: ...\nclass K(enum.StrEnum): ...", ["A"]),
        ("class A:\n    class Inner: ...", ["A"]),
        ("def f() -> None:\n    class Local: ...", []),
    ],
)
def test_public_classes(source, expected):
    assert public_classes(ast.parse(source)) == expected
