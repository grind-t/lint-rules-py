from collections.abc import Iterable, Iterator
from pathlib import Path


def read_fs_source_files(roots: Iterable[str]) -> Iterator[tuple[str, str]]:
    """Python files from the local filesystem."""
    for root in roots:
        for path in sorted(Path(root).rglob("*.py")):
            yield str(path), path.read_text(encoding="utf-8")
