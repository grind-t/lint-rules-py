from lint_rules._core.layout.crowded_directories import crowded_directories
from lint_rules._core.layout.crowded_directory_violation import (
    CrowdedDirectoryViolation,
)
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile

_LIMIT = 10


class CheckCrowdedDirectories:
    def __init__(self) -> None:
        self._paths: list[str] = []

    def visit(self, file: ParsedFile) -> None:
        self._paths.append(file.path)

    def finish(self) -> list[Violation]:
        return [
            CrowdedDirectoryViolation(directory, modules=modules, limit=_LIMIT)
            for directory, modules in crowded_directories(self._paths, _LIMIT)
        ]
