from lint_rules._stateless_computations.module_parts import module_parts


def qualified_module_name(path: str, root: str) -> str | None:
    """Dotted name of the module the file defines under ``root``, if any."""
    parts = module_parts(path, root)
    return ".".join(parts) if parts else None
