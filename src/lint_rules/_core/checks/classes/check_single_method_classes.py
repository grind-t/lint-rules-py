from lint_rules._core.classes.single_method_class_violation import (
    SingleMethodClassViolation,
)
from lint_rules._core.classes.single_method_classes import single_method_classes
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile

_MARKER = "# allow-single-method-classes"


def check_single_method_classes(file: ParsedFile) -> list[Violation]:
    if _MARKER in file.source:
        return []
    return [
        SingleMethodClassViolation(file.path, location, cls=cls, method=method)
        for cls, method, location in single_method_classes(file.tree)
    ]
