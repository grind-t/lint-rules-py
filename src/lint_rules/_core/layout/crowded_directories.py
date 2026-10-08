from collections import Counter
from collections.abc import Iterable

_PACKAGE_INIT = "__init__.py"


def _directory(path: str) -> str:
    return path.rpartition("/")[0] or "."


def crowded_directories(paths: Iterable[str], limit: int) -> list[tuple[str, int]]:
    """``(directory, count)`` for every directory with more than ``limit`` modules.

    Only ``.py`` files directly in the directory count; ``__init__.py`` and
    subdirectories do not.
    """
    counts = Counter(
        _directory(path)
        for path in paths
        if path.endswith(".py")
        and not path.endswith(f"/{_PACKAGE_INIT}")
        and path != _PACKAGE_INIT
    )
    return sorted((d, n) for d, n in counts.items() if n > limit)
