import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_from_imports import ast_from_imports


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
        ("from lib import *", []),
        ("from .lib import app", []),
        ("import lib", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert ast_from_imports(ast.parse(source)) == expected
