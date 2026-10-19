from pathlib import PurePosixPath


def top_level_module_name(path: str, root: str) -> str | None:
    """Name of the top-level module the file defines under ``root``, if any.

    A ``.py`` file directly under the root is a top-level module, and the
    ``__init__.py`` of a directory directly under the root makes that directory
    a top-level package. Deeper files define no top-level modules.
    """
    file = PurePosixPath(path)
    if not file.is_relative_to(root):
        return None
    match file.relative_to(root).parts:
        case [module] if module.endswith(".py") and module != "__init__.py":
            return module.removesuffix(".py")
        case [package, init] if init == "__init__.py":
            return package
    return None
