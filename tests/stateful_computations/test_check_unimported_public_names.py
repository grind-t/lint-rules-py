from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation_unimported_public_name import (
    ViolationUnimportedPublicName,
)
from lint_rules._stateful_computations.check_unimported_public_names import (
    CheckUnimportedPublicNames,
)


def test_check_unimported_public_names(subtests, fake_project):
    cases = [
        fake_project.case(
            "passes name imported by another module",
            fake_project.project()
            .module("lib.b", "from lib.a import run")
            .check_module("lib.a", "def run(): ..."),
            expected=[],
        ),
        fake_project.case(
            "passes name re-exported in a top-level package",
            fake_project.project()
            .package("lib", "from lib.a import run")
            .check_module("lib.a", "def run(): ..."),
            expected=[],
        ),
        fake_project.case(
            "passes private name",
            fake_project.project().check_module("lib.a", "def _run(): ..."),
            expected=[],
        ),
        fake_project.case(
            "passes code in a top-level package",
            fake_project.project().check_package("lib", "def run(): ..."),
            expected=[],
        ),
        fake_project.case(
            "passes imported name",
            fake_project.project().check_module("lib.a", "from lib.b import run"),
            expected=[],
        ),
        fake_project.case(
            "reports name used only in its module",
            fake_project.project().check_module("lib.a", "def run(): ...\nrun()"),
            expected=[
                ViolationUnimportedPublicName(
                    "src/lib/a.py", SourceLocation(1, 1), name="run"
                )
            ],
        ),
        fake_project.case(
            "reports name imported from another module of the same name",
            fake_project.project()
            .module("lib.b", "from lib.c import run")
            .check_module("lib.a", "def run(): ..."),
            expected=[
                ViolationUnimportedPublicName(
                    "src/lib/a.py", SourceLocation(1, 1), name="run"
                )
            ],
        ),
        fake_project.case(
            "reports variable",
            fake_project.project().check_module("lib.a", "LIMIT = 1"),
            expected=[
                ViolationUnimportedPublicName(
                    "src/lib/a.py", SourceLocation(1, 1), name="LIMIT"
                )
            ],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert fake_project.check(project, CheckUnimportedPublicNames()) == expected
