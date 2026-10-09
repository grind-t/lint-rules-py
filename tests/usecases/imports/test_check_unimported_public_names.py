from fake_project import Project, case, check

from lint_rules._core.names.unimported_public_name_violation import (
    UnimportedPublicNameViolation,
)
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._usecases.check_unimported_public_names import (
    CheckUnimportedPublicNames,
)


def test_check_unimported_public_names(subtests):
    cases = [
        case(
            "passes name imported by another module",
            Project()
            .module("lib.b", "from lib.a import run")
            .check_module("lib.a", "def run(): ..."),
            expected=[],
        ),
        case(
            "passes name re-exported in a top-level package",
            Project()
            .package("lib", "from lib.a import run")
            .check_module("lib.a", "def run(): ..."),
            expected=[],
        ),
        case(
            "passes private name",
            Project().check_module("lib.a", "def _run(): ..."),
            expected=[],
        ),
        case(
            "passes code in a top-level package",
            Project().check_package("lib", "def run(): ..."),
            expected=[],
        ),
        case(
            "passes imported name",
            Project().check_module("lib.a", "from lib.b import run"),
            expected=[],
        ),
        case(
            "reports name used only in its module",
            Project().check_module("lib.a", "def run(): ...\nrun()"),
            expected=[
                UnimportedPublicNameViolation(
                    "src/lib/a.py", SourceLocation(1, 1), name="run"
                )
            ],
        ),
        case(
            "reports name imported from another module of the same name",
            Project()
            .module("lib.b", "from lib.c import run")
            .check_module("lib.a", "def run(): ..."),
            expected=[
                UnimportedPublicNameViolation(
                    "src/lib/a.py", SourceLocation(1, 1), name="run"
                )
            ],
        ),
        case(
            "reports variable",
            Project().check_module("lib.a", "LIMIT = 1"),
            expected=[
                UnimportedPublicNameViolation(
                    "src/lib/a.py", SourceLocation(1, 1), name="LIMIT"
                )
            ],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert check(project, CheckUnimportedPublicNames()) == expected
