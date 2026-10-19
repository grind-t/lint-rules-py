from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_entities_public_function import (
    ViolationEntitiesPublicFunction,
)
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)


def check_entities_public_functions(file: ParsedFile) -> list[Violation]:
    """Entity modules define no public functions."""
    if "_entities" not in file.path.split("/"):
        return []
    return [
        ViolationEntitiesPublicFunction(file.path, location, name=name)
        for name, location in ast_public_functions(file.tree)
    ]
