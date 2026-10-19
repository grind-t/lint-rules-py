from lint_rules._entities.violation_non_empty_init import ViolationNonEmptyInit
from lint_rules._stateless_computations.check_non_empty_inits import (
    check_non_empty_inits,
)


def test_non_empty_inits(subtests, fake_project):
    cases = [
        fake_project.case(
            "passes re-export in top-level package",
            fake_project.project().check_package("lib", "from lib.app import run"),
            expected=[],
        ),
        fake_project.case(
            "passes re-export in another top-level package",
            fake_project.project()
            .package("lib")
            .check_package("other", "from lib.app import run"),
            expected=[],
        ),
        fake_project.case(
            "passes empty nested package",
            fake_project.project().package("lib").check_package("lib.core", ""),
            expected=[],
        ),
        fake_project.case(
            "passes comment-only nested package",
            fake_project.project().check_package("lib.core", "# nothing here"),
            expected=[],
        ),
        fake_project.case(
            "reports re-export in nested package",
            fake_project.project().check_package(
                "lib.core", "from lib.core.app import run"
            ),
            expected=[ViolationNonEmptyInit("src/lib/core/__init__.py")],
        ),
        fake_project.case(
            "reports docstring in nested package",
            fake_project.project().check_package("lib.core", '"""Core."""'),
            expected=[ViolationNonEmptyInit("src/lib/core/__init__.py")],
        ),
        fake_project.case(
            "passes code in a module",
            fake_project.project().check_module("lib.core.app", "x = 1"),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert fake_project.check(project, check_non_empty_inits) == expected
