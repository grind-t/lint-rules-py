import ast

from lint_rules._core.violation import Violation
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)


def check(source: str) -> list[Violation]:
    return check_single_method_classes("a.py", source, ast.parse(source))


def test_reports_class_with_single_method():
    assert check("x = 1\n\nclass A:\n    def run(self): ...") == [
        Violation(
            "a.py",
            "line 3: class A has a single method run; "
            "use a function, a Callable alias or a Protocol with __call__",
        )
    ]


def test_passes_module_without_classes():
    assert check("def run(): ...") == []


def test_marker_disables_check():
    assert (
        check("# allow-single-method-classes\nclass A:\n    def run(self): ...") == []
    )
