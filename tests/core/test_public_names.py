import ast

from lint_rules._core.names.public_names import public_names
from lint_rules._core.source.source_location import SourceLocation


def test_public_names(subtests):
    cases = [
        ("def f(): ...", ["f"]),
        ("async def f(): ...", ["f"]),
        ("class A: ...", ["A"]),
        ("X = 1", ["X"]),
        ("X: int = 1", ["X"]),
        ("X: int", ["X"]),
        ("type X = int", ["X"]),
        ("A = B = 1", ["A", "B"]),
        ("_x = 1\ndef _f(): ...\nclass _A: ...", []),
        ("__all__ = []", []),
        ("from a import b\nimport c", []),
        ("class A:\n    x = 1\n    def f(self): ...", ["A"]),
        ("def f():\n    x = 1", ["f"]),
        ("a, b = 1, 2", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            found = public_names(ast.parse(source))
            assert [name for name, _ in found] == expected


def test_public_names_location():
    found = public_names(ast.parse("x = 1\n\ndef f(): ..."))
    assert found == [("x", SourceLocation(1, 1)), ("f", SourceLocation(3, 1))]
