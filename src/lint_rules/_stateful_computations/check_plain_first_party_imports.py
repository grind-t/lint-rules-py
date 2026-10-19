from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.plain_import_violation import (
    PlainFirstPartyImportViolation,
)
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._stateless_computations.first_party import is_first_party
from lint_rules._stateless_computations.plain_imports import plain_imports
from lint_rules._stateless_computations.top_level_module import top_level_module


class CheckPlainFirstPartyImports:
    def __init__(self) -> None:
        self._top_level_modules: set[str] = set()
        self._imports: list[tuple[str, str, SourceLocation]] = []

    def visit(self, file: ParsedFile) -> None:
        if name := top_level_module(file.path, file.root):
            self._top_level_modules.add(name)
        self._imports.extend(
            (file.path, module, location)
            for module, location in plain_imports(file.tree)
        )

    def finish(self) -> list[Violation]:
        return [
            PlainFirstPartyImportViolation(path, location, module=module)
            for path, module, location in self._imports
            if is_first_party(module, self._top_level_modules)
        ]
