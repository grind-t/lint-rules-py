PACKAGE_INIT = "__init__.py"


def is_package_init(path: str) -> bool:
    """Whether the path names a package's ``__init__.py``."""
    return path.rpartition("/")[2] == PACKAGE_INIT
