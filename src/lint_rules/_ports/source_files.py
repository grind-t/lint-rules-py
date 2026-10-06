from collections.abc import Iterable
from typing import Protocol


class SourceFiles(Protocol):
    def read_all(self, roots: Iterable[str]) -> Iterable[tuple[str, str]]:
        """Yield ``(path, source)`` for every Python file under ``roots``."""
        ...
