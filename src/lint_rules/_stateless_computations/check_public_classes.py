from lint_rules._entities.multiple_public_classes_violation import (
    MultiplePublicClassesViolation,
)
from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._stateless_computations.public_classes import public_classes

_MARKER = "# allow-multiple-public-classes"


def check_public_classes(file: ParsedFile) -> list[Violation]:
    if _MARKER in file.source:
        return []
    classes = public_classes(file.tree)
    if len(classes) <= 1:
        return []
    return [MultiplePublicClassesViolation(file.path, classes=tuple(classes))]
