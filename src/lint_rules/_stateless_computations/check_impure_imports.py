from lint_rules._entities.impure_import_violation import ImpureImportViolation
from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._stateless_computations.impure_imports import impure_imports

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
        ImpureImportViolation(file.path, location, statement=statement)
        for statement, location in impure_imports(file.tree)
    ]
