from lint_rules._core.reexports.module_getattr_violation import ModuleGetattrViolation
from lint_rules._usecases.reexports.check_module_getattr import check_module_getattr


def test_module_getattr(subtests, fake_project):
    cases = [
        fake_project.case(
            "reports def __getattr__",
            fake_project.project().check_module("app", "def __getattr__(name): ..."),
            expected=[ModuleGetattrViolation("src/app.py")],
        ),
        # __dir__ only affects dir() and adds no names.
        fake_project.case(
            "passes __dir__",
            fake_project.project().check_module("app", "def __dir__(): ..."),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert fake_project.check(project, check_module_getattr) == expected
