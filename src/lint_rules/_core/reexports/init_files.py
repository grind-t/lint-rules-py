from pathlib import PurePosixPath

from lint_rules._core.shared.package_init import PACKAGE_INIT


def is_top_level_init(path: str, root: str) -> bool:
    """Whether the file is the ``__init__.py`` of a top-level package.

    That is a directory directly under ``root``, or ``root`` itself.
    """
    file = PurePosixPath(path)
    if not file.is_relative_to(root):
        return False
    match file.relative_to(root).parts:
        case [init] | [_, init]:
            return init == PACKAGE_INIT
    return False
