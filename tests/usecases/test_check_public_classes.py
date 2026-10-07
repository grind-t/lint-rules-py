import ast

from lint_rules._core.violation import Violation
from lint_rules._usecases.check_public_classes import check_public_classes


def check(source: str) -> list[Violation]:
    return check_public_classes("a.py", source, ast.parse(source))


def test_reports_module_with_two_public_classes():
    assert check("class A: ...\nclass B: ...") == [
        Violation("a.py", "2 public classes (A, B); split them into separate modules")
    ]


def test_passes_module_with_one_public_class():
    assert check("class A: ...") == []


def test_marker_disables_check():
    assert check("# allow-multiple-public-classes\nclass A: ...\nclass B: ...") == []


def test_str_has_no_location():
    [violation] = check("class A: ...\nclass B: ...")
    assert str(violation) == (
        "a.py: 2 public classes (A, B); split them into separate modules"
    )
