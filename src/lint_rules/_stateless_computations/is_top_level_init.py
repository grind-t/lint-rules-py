from lint_rules._stateless_computations.is_package_init import is_package_init
from lint_rules._stateless_computations.module_parts import module_parts


def is_top_level_init(path: str, root: str) -> bool:
    """Whether the file is the ``__init__.py`` of a top-level package.

    That is a directory directly under ``root``, or ``root`` itself.
    """
    parts = module_parts(path, root)
    return is_package_init(path) and parts is not None and len(parts) <= 1
