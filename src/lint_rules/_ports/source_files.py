from collections.abc import Iterable
from typing import Protocol

from lint_rules._core.source_file import SourceFile


class ReadSourceFiles(Protocol):
    def __call__(self, roots: Iterable[str]) -> Iterable[SourceFile]:
        """Yield every Python file under ``roots``."""
        ...
