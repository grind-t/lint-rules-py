from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_stateless_public_class import (
    ViolationStatelessPublicClass,
)
from lint_rules._stateless_computations.ast_public_non_protocol_classes import (
    ast_public_non_protocol_classes,
)
from lint_rules._stateless_computations.is_stateless_module import (
    is_stateless_module,
)


def check_stateless_public_classes(file: ParsedFile) -> list[Violation]:
    """Stateless modules define no public classes; Protocol ports are allowed."""
    if not is_stateless_module(file.path):
        return []
    return [
        ViolationStatelessPublicClass(file.path, location, name=name)
        for name, location in ast_public_non_protocol_classes(file.tree)
    ]
