from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_too_many_public_classes import (
    ViolationTooManyPublicClasses,
)
from lint_rules._stateless_computations.ast_public_classes import ast_public_classes
from lint_rules._stateless_computations.layer_package import layer_package

_MAX_PUBLIC_CLASSES = {
    "_entities": 1,
    "_stateless_computations": 0,
    "_stateless_workflows": 0,
    "_stateless_effects": 0,
    "_stateful_computations": 1,
    "_stateful_workflows": 1,
    "_stateful_effects": 1,
}


def check_public_classes(file: ParsedFile) -> list[Violation]:
    """Modules of a layer package have at most its limit of public classes."""
    package = layer_package(file.path)
    if package is None:
        return []
    limit = _MAX_PUBLIC_CLASSES[package]
    classes = ast_public_classes(file.tree)
    if len(classes) <= limit:
        return []
    return [
        ViolationTooManyPublicClasses(
            file.path,
            classes[limit][1],
            package=package,
            limit=limit,
            classes=tuple(name for name, _ in classes),
        )
    ]
