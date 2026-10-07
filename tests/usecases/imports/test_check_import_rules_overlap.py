"""Imports that more than one import rule could report."""

import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violation import Violation


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
                Violation(
                    "src/lib/_usecases/app.py",
                    'relative import; use "from lib._core import ..." instead',
                    SourceLocation(1, 1),
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
                Violation(
                    "src/lib/_usecases/app.py",
                    'relative import; use "from lib._core import ..." instead',
                    SourceLocation(1, 1),
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
                Violation(
                    "src/lib/_usecases/app.py",
                    'relative import; use "from lib._usecases.lazy import ..." instead',
                    SourceLocation(1, 1),
                ),
                Violation(
                    "src/lib/_usecases/app.py",
                    "module-level __getattr__ makes names dynamic; "
                    "define them explicitly",
                ),
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
                Violation(
                    "src/lib/app.py",
                    '"from lib._core import *" hides which names are used; '
                    "import them explicitly",
                    SourceLocation(1, 23),
                )
            ],
        ),
    ],
)
def test_import_rules_overlap(project, expected):
    assert check(project) == expected
