from lint_rules._entities.multiple_public_classes_violation import (
    MultiplePublicClassesViolation,
)
from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.violation import Violation
from lint_rules._stateless_computations.check_public_classes import check_public_classes
from lint_rules._stateless_computations.parse_file import parse_file


def check(source: str) -> list[Violation]:
    return check_public_classes(parse_file(SourceFile("src", "a.py", source)))


def test_reports_module_with_two_public_classes():
    assert check("class A: ...\nclass B: ...") == [
        MultiplePublicClassesViolation("a.py", classes=("A", "B"))
    ]


def test_passes_module_with_one_public_class():
    assert check("class A: ...") == []


def test_marker_disables_check():
    assert check("# allow-multiple-public-classes\nclass A: ...\nclass B: ...") == []
