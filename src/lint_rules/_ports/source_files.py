from collections.abc import Iterable
from typing import Protocol

from lint_rules._core.source.source_file import SourceFile


class ReadSourceFiles(Protocol):
    def __call__(self, root: str) -> Iterable[SourceFile]:
        """Yield every Python file under ``root``."""
        ...
