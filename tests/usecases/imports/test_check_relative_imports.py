import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violations.relative_import import RelativeImportViolation


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
                RelativeImportViolation(
                    "src/lib/_usecases/app.py",
                    SourceLocation(1, 1),
                    absolute="lib._core.greeting",
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
                RelativeImportViolation(
                    "src/lib/_usecases/app.py",
                    SourceLocation(1, 1),
                    absolute="lib._usecases",
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
                RelativeImportViolation(
                    "src/lib/_usecases/app.py", SourceLocation(1, 1), absolute=None
                )
            ],
        ),
        case(
            "resolves package __init__.py against the package itself",
            Project()
            .package("lib")
            .check_package("lib._core", "from .greeting import format_greeting"),
            expected=[
                RelativeImportViolation(
                    "src/lib/_core/__init__.py",
                    SourceLocation(1, 1),
                    absolute="lib._core.greeting",
                )
            ],
        ),
        # Not importable, but still checked.
        case(
            "checks file without module name",
            Project().package("lib").check_file("my-dir/x.py", "from . import x"),
            expected=[
                RelativeImportViolation(
                    "src/my-dir/x.py", SourceLocation(1, 1), absolute=None
                )
            ],
        ),
    ],
)
def test_relative_import(project, expected):
    assert check(project) == expected
