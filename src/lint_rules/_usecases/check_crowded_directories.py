from lint_rules._core.crowded_directories import crowded_directories
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.violation import Violation
from lint_rules._core.violations.crowded_directory import CrowdedDirectoryViolation

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
