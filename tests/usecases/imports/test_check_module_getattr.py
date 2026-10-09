from lint_rules._core.reexports.module_getattr_violation import ModuleGetattrViolation
from lint_rules._usecases.reexports.check_module_getattr import check_module_getattr

_BINDING_FORMS = [
    "def __getattr__(name): ...",
    "__getattr__ = _lazy",
    "from lib import __getattr__",
    "for __getattr__ in hooks: ...",
    "if x:\n    def __getattr__(name): ...",
]

# Methods and nested functions do not bind a module attribute. __dir__ only
# affects dir() and adds no names.
_NON_BINDING_FORMS = [
    "print(__getattr__)",
    "class C:\n    def __getattr__(self, name): ...",
    "def f():\n    def __getattr__(name): ...",
    "def __dir__(): ...",
]


def test_module_getattr(subtests, fake_project):
    cases = [
        fake_project.case(
            f"reports {source!r}",
            fake_project.project().check_module("app", source),
            expected=[ModuleGetattrViolation("src/app.py")],
        )
        for source in _BINDING_FORMS
    ] + [
        fake_project.case(
            f"passes {source!r}",
            fake_project.project().check_module("app", source),
            expected=[],
        )
        for source in _NON_BINDING_FORMS
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert fake_project.check(project, check_module_getattr) == expected
