from lint_rules._entities.single_method_class_violation import (
    SingleMethodClassViolation,
)
from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._stateless_computations.check_single_method_classes import (
    check_single_method_classes,
)
from lint_rules._stateless_computations.parse_file import parse_file


def check(source: str) -> list[Violation]:
    return check_single_method_classes(parse_file(SourceFile("src", "a.py", source)))


def test_reports_class_with_single_method():
    assert check("x = 1\n\nclass A:\n    def run(self): ...") == [
        SingleMethodClassViolation("a.py", SourceLocation(3, 1), cls="A", method="run")
    ]


def test_marker_disables_check():
    assert (
        check("# allow-single-method-classes\nclass A:\n    def run(self): ...") == []
    )
