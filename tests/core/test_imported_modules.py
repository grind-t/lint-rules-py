import ast

import pytest

from lint_rules._core.imports.imported_modules import imported_modules


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("import a, b.c", {"a", "b.c"}),
        ("import a as x", {"a"}),
        ("from a import b, c as d", {"a", "a.b", "a.c"}),
        ("from a import *", {"a"}),
        ("from . import b\nfrom .a import c", set()),
        ("def f():\n    from a import b", {"a", "a.b"}),
        ("x = 1", set()),
    ],
)
def test_imported_modules(source, expected):
    assert imported_modules(ast.parse(source)) == expected
