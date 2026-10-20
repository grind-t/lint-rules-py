from pathlib import PurePosixPath


def module_parts(path: str, root: str) -> tuple[str, ...] | None:
    """Parts of the dotted name of the module the file defines under ``root``.

    A package's ``__init__.py`` stands for the package, so the root's own
    ``__init__.py`` has no parts; non-``.py`` files and files outside the
    root define no module.
    """
    file = PurePosixPath(path)
    if file.suffix != ".py" or not file.is_relative_to(root):
        return None
    parts = file.relative_to(root).with_suffix("").parts
    return parts[:-1] if parts[-1] == "__init__" else parts
