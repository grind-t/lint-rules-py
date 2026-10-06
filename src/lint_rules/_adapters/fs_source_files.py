from collections.abc import Iterable, Iterator
from pathlib import Path


class FsSourceFiles:
    """Python files from the local filesystem."""

    def read_all(self, roots: Iterable[str]) -> Iterator[tuple[str, str]]:
        for root in roots:
            for path in sorted(Path(root).rglob("*.py")):
                yield str(path), path.read_text(encoding="utf-8")
