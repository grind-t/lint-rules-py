from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_stateful_public_function import (
    ViolationStatefulPublicFunction,
)
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)
from lint_rules._stateless_computations.is_stateful_module import (
    is_stateful_module,
)


def check_stateful_public_functions(file: ParsedFile) -> list[Violation]:
    """Stateful modules define no public functions."""
    if not is_stateful_module(file.path):
        return []
    return [
        ViolationStatefulPublicFunction(file.path, location, name=name)
        for name, location in ast_public_functions(file.tree)
    ]
