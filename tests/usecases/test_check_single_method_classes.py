from lint_rules._core.classes.single_method_class_violation import (
    SingleMethodClassViolation,
)
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_file import SourceFile
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)


def check(source: str) -> list[Violation]:
    return check_single_method_classes(ParsedFile(SourceFile(".", "a.py", source)))


def test_reports_class_with_single_method():
    assert check("x = 1\n\nclass A:\n    def run(self): ...") == [
        SingleMethodClassViolation("a.py", SourceLocation(3, 1), cls="A", method="run")
    ]


def test_marker_disables_check():
    assert (
        check("# allow-single-method-classes\nclass A:\n    def run(self): ...") == []
    )
