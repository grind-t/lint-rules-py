from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.unimported_public_name_violation import (
    UnimportedPublicNameViolation,
)
from lint_rules._entities.violation import Violation
from lint_rules._stateless_computations.from_imports import from_imports
from lint_rules._stateless_computations.init_files import is_top_level_init
from lint_rules._stateless_computations.module_name import module_name
from lint_rules._stateless_computations.public_names import public_names


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
