from lint_rules._core.classes.multiple_public_classes_violation import (
    MultiplePublicClassesViolation,
)
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_file import SourceFile
from lint_rules._usecases.check_public_classes import check_public_classes


def check(source: str) -> list[Violation]:
    return check_public_classes(ParsedFile(SourceFile("src", "a.py", source)))


def test_reports_module_with_two_public_classes():
    assert check("class A: ...\nclass B: ...") == [
        MultiplePublicClassesViolation("a.py", classes=("A", "B"))
    ]


def test_passes_module_with_one_public_class():
    assert check("class A: ...") == []


def test_marker_disables_check():
    assert check("# allow-multiple-public-classes\nclass A: ...\nclass B: ...") == []
