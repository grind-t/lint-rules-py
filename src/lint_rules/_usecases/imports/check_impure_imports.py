from lint_rules._core.imports.impure_import_violation import ImpureImportViolation
from lint_rules._core.imports.impure_imports import impure_imports
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile

_NO_IO_LAYERS = frozenset({"_core", "_ports", "_usecases"})


def check_impure_imports(file: ParsedFile) -> list[Violation]:
    """Layers that do no I/O may import only the pure names of I/O modules."""
    if _NO_IO_LAYERS.isdisjoint(file.path.split("/")):
        return []
    return [
        ImpureImportViolation(file.path, location, statement=statement)
        for statement, location in impure_imports(file.tree)
    ]
