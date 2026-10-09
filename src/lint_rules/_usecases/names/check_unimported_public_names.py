from lint_rules._core.imports.from_imports import from_imports
from lint_rules._core.names.public_names import public_names
from lint_rules._core.names.unimported_public_name_violation import (
    UnimportedPublicNameViolation,
)
from lint_rules._core.reexports.init_files import is_top_level_init
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.module_name import module_name
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_location import SourceLocation


class CheckUnimportedPublicNames:
    def __init__(self) -> None:
        self._imported: set[tuple[str, str]] = set()
        self._defined: list[tuple[str, str, str, SourceLocation]] = []

    def visit(self, file: ParsedFile) -> None:
        self._imported.update(
            (module, name) for module, name, _ in from_imports(file.tree)
        )
        module = module_name(file.path, file.root)
        if module is None or is_top_level_init(file.path, file.root):
            return
        self._defined.extend(
            (file.path, module, name, location)
            for name, location in public_names(file.tree)
        )

    def finish(self) -> list[Violation]:
        return [
            UnimportedPublicNameViolation(path, location, name=name)
            for path, module, name, location in self._defined
            if (module, name) not in self._imported
        ]
