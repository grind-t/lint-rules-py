from collections.abc import Iterable, Iterator
from pathlib import Path

from lint_rules._core.source_file import SourceFile


def read_fs_source_files(roots: Iterable[str]) -> Iterator[SourceFile]:
    """Python files from the local filesystem."""
    for root in roots:
        for path in sorted(Path(root).rglob("*.py")):
            yield SourceFile(root, str(path), path.read_text(encoding="utf-8"))
