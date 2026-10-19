from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_multiple_public_functions import (
    ViolationMultiplePublicFunctions,
)
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)
from lint_rules._stateless_computations.is_stateless_module import (
    is_stateless_module,
)


def check_stateless_public_functions(file: ParsedFile) -> list[Violation]:
    """Stateless modules have at most one public function."""
    if not is_stateless_module(file.path):
        return []
    functions = ast_public_functions(file.tree)
    if len(functions) <= 1:
        return []
    return [ViolationMultiplePublicFunctions(file.path, functions=tuple(functions))]
