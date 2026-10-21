from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_unimported_public_name import (
    ViolationUnimportedPublicName,
)
from lint_rules._stateless_computations.ast_from_imports import ast_from_imports
from lint_rules._stateless_computations.ast_public_names import ast_public_names
from lint_rules._stateless_computations.is_top_level_init import is_top_level_init
from lint_rules._stateless_computations.qualified_module_name import (
    qualified_module_name,
)


class CheckUnimportedPublicNames:
    def __init__(self) -> None:
        self._imported_names: set[tuple[str, str]] = set()
        self._public_names: list[tuple[str, str, str, SourceLocation]] = []

    def visit(self, file: ParsedFile) -> None:
        self._imported_names.update(
            (module, name) for module, name, _ in ast_from_imports(file.tree)
        )
        module = qualified_module_name(file.path, file.root)
        if module is None or is_top_level_init(file.path, file.root):
            return
        self._public_names.extend(
            (file.path, module, name, location)
            for name, location in ast_public_names(file.tree)
        )

    def finish(self) -> list[Violation]:
        return [
            ViolationUnimportedPublicName(path, location, name=name)
            for path, module, name, location in self._public_names
            if (module, name) not in self._imported_names
        ]
