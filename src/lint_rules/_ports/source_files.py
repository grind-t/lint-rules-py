from collections.abc import Iterable
from typing import Protocol


class ReadSourceFiles(Protocol):
    def __call__(self, roots: Iterable[str]) -> Iterable[tuple[str, str]]:
        """Yield ``(path, source)`` for every Python file under ``roots``."""
        ...
