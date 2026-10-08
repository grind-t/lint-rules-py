from lint_rules._core.imports.first_party import is_first_party
from lint_rules._core.imports.first_party_module_from_import_violation import (
    FirstPartyModuleFromImportViolation,
)
from lint_rules._core.imports.from_imports import from_imports
from lint_rules._core.imports.top_level_module import top_level_module
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.module_name import module_name
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_location import SourceLocation


class CheckFirstPartyModuleFromImports:
    def __init__(self) -> None:
        self._top_level_modules: set[str] = set()
        self._modules: set[str] = set()
        self._imports: list[tuple[str, str, str, SourceLocation]] = []

    def visit(self, file: ParsedFile) -> None:
        if name := top_level_module(file.path, file.root):
            self._top_level_modules.add(name)
        if name := module_name(file.path, file.root):
            self._modules.add(name)
        self._imports.extend(
            (file.path, module, name, location)
            for module, name, location in from_imports(file.tree)
        )

    def finish(self) -> list[Violation]:
        return [
            FirstPartyModuleFromImportViolation(
                path, location, module=module, name=name
            )
            for path, module, name, location in self._imports
            if is_first_party(module, self._top_level_modules)
            and f"{module}.{name}" in self._modules
        ]
