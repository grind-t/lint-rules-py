import ast

from lint_rules._core.imports.plain_imports import plain_imports
from lint_rules._core.source.source_location import SourceLocation


def test_plain_imports(subtests):
    cases = [
        ("import lib", [("lib", SourceLocation(1, 8))]),
        ("import lib.app as app", [("lib.app", SourceLocation(1, 8))]),
        (
            "import os, lib",
            [("os", SourceLocation(1, 8)), ("lib", SourceLocation(1, 12))],
        ),
        (
            "import b\ndef f():\n    import a",
            [("b", SourceLocation(1, 8)), ("a", SourceLocation(3, 12))],
        ),
        ("from lib import app", []),
        ("x = __import__('lib')", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert plain_imports(ast.parse(source)) == expected
