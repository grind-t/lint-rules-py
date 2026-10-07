import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violation import Violation


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports with absolute module name",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module(
                "lib._usecases.app", "from .._core.greeting import format_greeting"
            ),
            expected=[
                Violation(
                    "src/lib/_usecases/app.py",
                    'relative import; use "from lib._core.greeting import ..." instead',
                    SourceLocation(1, 1),
                )
            ],
        ),
        case(
            "reports dot-only import with anchor package",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from . import greet"),
            expected=[
                Violation(
                    "src/lib/_usecases/app.py",
                    'relative import; use "from lib._usecases import ..." instead',
                    SourceLocation(1, 1),
                )
            ],
        ),
        case(
            "reports import beyond top-level package without name",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from ... import x"),
            expected=[
                Violation(
                    "src/lib/_usecases/app.py",
                    "relative import; use an absolute import instead",
                    SourceLocation(1, 1),
                )
            ],
        ),
        case(
            "resolves package __init__.py against the package itself",
            Project()
            .package("lib")
            .check_package("lib._core", "from .greeting import format_greeting"),
            expected=[
                Violation(
                    "src/lib/_core/__init__.py",
                    'relative import; use "from lib._core.greeting import ..." instead',
                    SourceLocation(1, 1),
                )
            ],
        ),
        # Not importable, but still checked.
        case(
            "checks file without module name",
            Project().package("lib").check_file("my-dir/x.py", "from . import x"),
            expected=[
                Violation(
                    "src/my-dir/x.py",
                    "relative import; use an absolute import instead",
                    SourceLocation(1, 1),
                )
            ],
        ),
    ],
)
def test_relative_import(project, expected):
    assert check(project) == expected
