import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violations.star_import import StarImportViolation


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports first-party module",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .check_module("lib.app", "from lib._core.greeting import *"),
            expected=[
                StarImportViolation(
                    "src/lib/app.py", SourceLocation(1, 32), module="lib._core.greeting"
                )
            ],
        ),
        case(
            "passes third-party module",
            Project().check_module("app", "from os.path import *"),
            expected=[],
        ),
    ],
)
def test_star_import(project, expected):
    assert check(project) == expected
