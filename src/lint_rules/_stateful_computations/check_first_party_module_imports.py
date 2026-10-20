from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_first_party_module_import import (
    ViolationFirstPartyModuleImport,
)
from lint_rules._entities.violation_first_party_module_import_from import (
    ViolationFirstPartyModuleImportFrom,
)
from lint_rules._stateless_computations.ast_from_imports import ast_from_imports
from lint_rules._stateless_computations.ast_imports import ast_imports
from lint_rules._stateless_computations.is_first_party_module import (
    is_first_party_module,
)
from lint_rules._stateless_computations.qualified_module_name import (
    qualified_module_name,
)
from lint_rules._stateless_computations.top_level_module_name import (
    top_level_module_name,
)


class CheckFirstPartyModuleImports:
    """``import pkg.mod`` and ``from pkg import mod`` of first-party modules."""

    def __init__(self) -> None:
        self._top_level_modules: set[str] = set()
        self._modules: set[str] = set()
        self._imports: list[tuple[str, str, SourceLocation]] = []
        self._from_imports: list[tuple[str, str, str, SourceLocation]] = []

    def visit(self, file: ParsedFile) -> None:
        if name := top_level_module_name(file.path, file.root):
            self._top_level_modules.add(name)
        if name := qualified_module_name(file.path, file.root):
            self._modules.add(name)
        self._imports.extend(
            (file.path, module, location) for module, location in ast_imports(file.tree)
        )
        self._from_imports.extend(
            (file.path, module, name, location)
            for module, name, location in ast_from_imports(file.tree)
        )

    def finish(self) -> list[Violation]:
        violations: list[Violation] = [
            ViolationFirstPartyModuleImport(path, location, module=module)
            for path, module, location in self._imports
            if is_first_party_module(module, self._top_level_modules)
        ]
        violations.extend(
            ViolationFirstPartyModuleImportFrom(
                path, location, module=module, name=name
            )
            for path, module, name, location in self._from_imports
            if is_first_party_module(module, self._top_level_modules)
            and f"{module}.{name}" in self._modules
        )
        return violations
