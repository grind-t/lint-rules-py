from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_too_many_public_functions import (
    ViolationTooManyPublicFunctions,
)
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)
from lint_rules._stateless_computations.layer_package import layer_package

_MAX_PUBLIC_FUNCTIONS = {
    "_entities": 0,
    "_stateless_computations": 1,
    "_stateless_workflows": 1,
    "_stateless_effects": 1,
    "_stateful_computations": 0,
    "_stateful_workflows": 0,
    "_stateful_effects": 0,
}


def check_public_functions(file: ParsedFile) -> list[Violation]:
    """Modules of a layer package have at most its limit of public functions."""
    package = layer_package(file.path)
    if package is None:
        return []
    limit = _MAX_PUBLIC_FUNCTIONS[package]
    functions = ast_public_functions(file.tree)
    if len(functions) <= limit:
        return []
    return [
        ViolationTooManyPublicFunctions(
            file.path,
            functions[limit][1],
            package=package,
            limit=limit,
            functions=tuple(name for name, _ in functions),
        )
    ]
