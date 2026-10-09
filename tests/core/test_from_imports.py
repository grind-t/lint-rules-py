import ast

from lint_rules._core.imports.from_imports import from_imports
from lint_rules._core.source.source_location import SourceLocation


def test_from_imports(subtests):
    cases = [
        ("from lib import app", [("lib", "app", SourceLocation(1, 17))]),
        ("from lib.core import app", [("lib.core", "app", SourceLocation(1, 22))]),
        ("from lib import app as a", [("lib", "app", SourceLocation(1, 17))]),
        (
            "from lib import a, b",
            [("lib", "a", SourceLocation(1, 17)), ("lib", "b", SourceLocation(1, 20))],
        ),
        (
            "from b import x\ndef f():\n    from a import y",
            [("b", "x", SourceLocation(1, 15)), ("a", "y", SourceLocation(3, 19))],
        ),
        (
            "try:\n    from a import x\nexcept ImportError: ...",
            [("a", "x", SourceLocation(2, 19))],
        ),
        ("from lib import *", []),
        ("from . import app", []),
        ("from .lib import app", []),
        ("import lib", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert from_imports(ast.parse(source)) == expected
