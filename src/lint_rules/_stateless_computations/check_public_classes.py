from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_multiple_public_classes import (
    ViolationMultiplePublicClasses,
)
from lint_rules._stateless_computations.ast_public_classes import ast_public_classes


def check_public_classes(file: ParsedFile) -> list[Violation]:
    classes = ast_public_classes(file.tree)
    if len(classes) <= 1:
        return []
    return [ViolationMultiplePublicClasses(file.path, classes=tuple(classes))]
