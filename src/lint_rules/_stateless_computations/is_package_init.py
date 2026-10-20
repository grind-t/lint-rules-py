from pathlib import PurePosixPath


def is_package_init(path: str) -> bool:
    """Whether the path names a package's ``__init__.py``."""
    return PurePosixPath(path).name == "__init__.py"
