from fake_project import Project, case, check

from lint_rules._core.reexports.module_getattr_violation import ModuleGetattrViolation
from lint_rules._usecases.check_module_getattr import check_module_getattr


def test_module_getattr(subtests):
    cases = [
        case(
            "reports def __getattr__",
            Project().check_module("app", "def __getattr__(name): ..."),
            expected=[ModuleGetattrViolation("src/app.py")],
        ),
        # __dir__ only affects dir() and adds no names.
        case(
            "passes __dir__",
            Project().check_module("app", "def __dir__(): ..."),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert check(project, check_module_getattr) == expected
