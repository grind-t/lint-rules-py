from pathlib import PurePosixPath

from lint_rules._core.shared.package_init import PACKAGE_INIT


def top_level_module(path: str, root: str) -> str | None:
    """Name of the top-level module the file defines under ``root``, if any.

    A ``.py`` file directly under the root is a top-level module, and the
    ``__init__.py`` of a directory directly under the root makes that directory
    a top-level package. Deeper files define no top-level modules.
    """
    file = PurePosixPath(path)
    if not file.is_relative_to(root):
        return None
    match file.relative_to(root).parts:
        case [module] if module.endswith(".py") and module != PACKAGE_INIT:
            return module.removesuffix(".py")
        case [package, init] if init == PACKAGE_INIT:
            return package
    return None
