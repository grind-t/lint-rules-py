from fake_project import Project, case, check

from lint_rules._core.reexports.non_empty_init_violation import NonEmptyInitViolation
from lint_rules._usecases.reexports.check_non_empty_inits import check_non_empty_inits


def test_non_empty_inits(subtests):
    cases = [
        case(
            "passes re-export in top-level package",
            Project().check_package("lib", "from lib.app import run"),
            expected=[],
        ),
        case(
            "passes re-export in another top-level package",
            Project().package("lib").check_package("other", "from lib.app import run"),
            expected=[],
        ),
        case(
            "passes empty nested package",
            Project().package("lib").check_package("lib.core", ""),
            expected=[],
        ),
        case(
            "passes comment-only nested package",
            Project().check_package("lib.core", "# nothing here"),
            expected=[],
        ),
        case(
            "reports re-export in nested package",
            Project().check_package("lib.core", "from lib.core.app import run"),
            expected=[NonEmptyInitViolation("src/lib/core/__init__.py")],
        ),
        case(
            "reports docstring in nested package",
            Project().check_package("lib.core", '"""Core."""'),
            expected=[NonEmptyInitViolation("src/lib/core/__init__.py")],
        ),
        case(
            "passes code in a module",
            Project().check_module("lib.core.app", "x = 1"),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert check(project, check_non_empty_inits) == expected
