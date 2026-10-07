import pytest
from fake_project import Project, case, check

from lint_rules._core.violations.module_getattr import ModuleGetattrViolation


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports def __getattr__",
            Project().check_module("app", "def __getattr__(name): ..."),
            expected=[ModuleGetattrViolation("src/app.py")],
        ),
        case(
            "reports __getattr__ assignment",
            Project().check_module("app", "__getattr__ = _lazy"),
            expected=[ModuleGetattrViolation("src/app.py")],
        ),
        # lib._lazy does not exist, so only the binding is reported.
        case(
            "reports imported __getattr__",
            Project()
            .package("lib")
            .check_module("lib.app", "from lib._lazy import __getattr__"),
            expected=[ModuleGetattrViolation("src/lib/app.py")],
        ),
        case(
            "reports __getattr__ in top-level block",
            Project().check_module(
                "app",
                """
                if sys.version_info < (3, 15):
                    def __getattr__(name): ...
                """,
            ),
            expected=[ModuleGetattrViolation("src/app.py")],
        ),
        case(
            "passes __getattr__ method",
            Project().check_module(
                "app",
                """
                class C(Base):
                    def __getattr__(self, name): ...
                """,
            ),
            expected=[],
        ),
        case(
            "passes local __getattr__ function",
            Project().check_module(
                "app",
                """
                def f():
                    def __getattr__(name): ...
                """,
            ),
            expected=[],
        ),
        # __dir__ only affects dir() and adds no names.
        case(
            "passes __dir__",
            Project().check_module("app", "def __dir__(): ..."),
            expected=[],
        ),
    ],
)
def test_module_getattr(project, expected):
    assert check(project) == expected
