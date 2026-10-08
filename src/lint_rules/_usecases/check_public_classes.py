from lint_rules._core.classes.multiple_public_classes_violation import (
    MultiplePublicClassesViolation,
)
from lint_rules._core.classes.public_classes import public_classes
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile

_MARKER = "# allow-multiple-public-classes"


def check_public_classes(file: ParsedFile) -> list[Violation]:
    if _MARKER in file.source:
        return []
    classes = public_classes(file.tree)
    if len(classes) <= 1:
        return []
    return [MultiplePublicClassesViolation(file.path, classes=tuple(classes))]
