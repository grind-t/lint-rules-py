from collections.abc import Iterator
from pathlib import Path

from lint_rules._core.source.source_file import SourceFile


def read_fs_source_files(root: str) -> Iterator[SourceFile]:
    """Python files from the local filesystem."""
    for path in sorted(Path(root).rglob("*.py")):
        yield SourceFile(root, str(path), path.read_text(encoding="utf-8"))
