"""Imports that more than one import rule could report."""

import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violations.module_getattr import ModuleGetattrViolation
from lint_rules._core.violations.relative_import import RelativeImportViolation
from lint_rules._core.violations.star_import import StarImportViolation


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        # One violation per statement; its aliases are not checked further, though
        # as absolute imports both would be reported.
        case(
            "reports relative import once per statement",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .package("lib._usecases")
            .check_module(
                "lib._usecases.app", "from .._core import greeting, format_greeting"
            ),
            expected=[
                RelativeImportViolation(
                    "src/lib/_usecases/app.py",
                    SourceLocation(1, 1),
                    absolute="lib._core",
                )
            ],
        ),
        case(
            "reports relative star import only as relative",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from .._core import *"),
            expected=[
                RelativeImportViolation(
                    "src/lib/_usecases/app.py",
                    SourceLocation(1, 1),
                    absolute="lib._core",
                )
            ],
        ),
        case(
            "reports __getattr__ binding separately from relative import",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from .lazy import __getattr__"),
            expected=[
                RelativeImportViolation(
                    "src/lib/_usecases/app.py",
                    SourceLocation(1, 1),
                    absolute="lib._usecases.lazy",
                ),
                ModuleGetattrViolation("src/lib/_usecases/app.py"),
            ],
        ),
        # The star import is reported instead of the package: one violation, not two.
        case(
            "reports star import from package only once",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib._core import *"),
            expected=[
                StarImportViolation(
                    "src/lib/app.py", SourceLocation(1, 23), module="lib._core"
                )
            ],
        ),
    ],
)
def test_import_rules_overlap(project, expected):
    assert check(project) == expected
