from pathlib import PurePosixPath

_PACKAGE_INIT = "__init__.py"


def is_top_level_init(path: str, root: str) -> bool:
    """Whether the file is the ``__init__.py`` of a top-level package.

    That is a directory directly under ``root``, or ``root`` itself.
    """
    file = PurePosixPath(path)
    if not file.is_relative_to(root):
        return False
    match file.relative_to(root).parts:
        case [init] | [_, init]:
            return init == _PACKAGE_INIT
    return False
