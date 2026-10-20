from lint_rules._stateless_computations.module_parts import module_parts


def top_level_module_name(path: str, root: str) -> str | None:
    """Name of the top-level module or package the file defines, if any.

    That is a ``.py`` file directly under ``root`` or the ``__init__.py`` of
    a directory directly under it.
    """
    match module_parts(path, root):
        case [name]:
            return name
    return None
