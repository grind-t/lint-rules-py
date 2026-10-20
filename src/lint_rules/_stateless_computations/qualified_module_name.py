from pathlib import PurePosixPath


def qualified_module_name(path: str, root: str) -> str | None:
    """Dotted name of the module the file defines under ``root``, if any.

    A package's ``__init__.py`` defines the package itself; the root's own
    ``__init__.py`` and files outside the root define no module.
    """
    file = PurePosixPath(path)
    if file.suffix != ".py" or not file.is_relative_to(root):
        return None
    parts = list(file.relative_to(root).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts) or None
