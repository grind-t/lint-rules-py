from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_impure_import import ViolationImpureImport
from lint_rules._stateless_computations.ast_impure_imports import ast_impure_imports
from lint_rules._stateless_computations.layer_of import layer_of


def check_impure_imports(file: ParsedFile) -> list[Violation]:
    """Layers that do no I/O may import only the pure names of I/O modules."""
    layer = layer_of(file.path)
    if layer is None or layer.does_io:
        return []
    return [
        ViolationImpureImport(file.path, location, statement=statement)
        for statement, location in ast_impure_imports(file.tree)
    ]
