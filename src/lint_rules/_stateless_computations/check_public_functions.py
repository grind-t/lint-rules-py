from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_multiple_public_functions import (
    ViolationMultiplePublicFunctions,
)
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)

_STATELESS_LAYERS = frozenset(
    {
        "_stateless_computations",
        "_stateless_workflows",
        "_stateless_effects",
    }
)


def check_public_functions(file: ParsedFile) -> list[Violation]:
    """Stateless modules have at most one public function."""
    if _STATELESS_LAYERS.isdisjoint(file.path.split("/")):
        return []
    functions = ast_public_functions(file.tree)
    if len(functions) <= 1:
        return []
    return [ViolationMultiplePublicFunctions(file.path, functions=tuple(functions))]
