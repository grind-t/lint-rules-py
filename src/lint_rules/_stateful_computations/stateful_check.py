from typing import Protocol, runtime_checkable

from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation


@runtime_checkable
class StatefulCheck(Protocol):
    """A check that needs every file before it can report, e.g. across files."""

    def visit(self, file: ParsedFile) -> None:
        """Collect what the check needs from one file."""
        ...

    def finish(self) -> list[Violation]:
        """Report once every file has been visited."""
        ...
