from lint_rules._core.imports.imported_modules import imported_modules
from lint_rules._core.layout.unshared_module_violation import UnsharedModuleViolation
from lint_rules._core.layout.unshared_modules import unshared_modules
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.module_name import module_name
from lint_rules._core.source.parsed_file import ParsedFile


class CheckUnsharedModules:
    def __init__(self, root: str) -> None:
        self._root = root
        self._imports: dict[str, set[str]] = {}
        self._modules: dict[str, str] = {}

    def visit(self, file: ParsedFile) -> None:
        self._imports[file.path] = imported_modules(file.tree)
        if name := module_name(file.path, self._root):
            self._modules[name] = file.path

    def finish(self) -> list[Violation]:
        return [
            UnsharedModuleViolation(path, features=features)
            for path, features in unshared_modules(self._imports, self._modules)
        ]
