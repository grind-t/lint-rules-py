from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_impure_import import ViolationImpureImport
from lint_rules._stateless_computations.ast_impure_imports import ast_impure_imports

_NO_IO_LAYERS = frozenset(
    {
        "_entities",
        "_stateless_computations",
        "_stateful_computations",
        "_stateless_workflows",
        "_stateful_workflows",
    }
)


def check_impure_imports(file: ParsedFile) -> list[Violation]:
    """Layers that do no I/O may import only the pure names of I/O modules."""
    if _NO_IO_LAYERS.isdisjoint(file.path.split("/")):
        return []
    return [
        ViolationImpureImport(file.path, location, statement=statement)
        for statement, location in ast_impure_imports(file.tree)
    ]
