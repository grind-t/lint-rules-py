import ast


def base_name(base: ast.expr) -> str:
    """Last name component of a base class expression, e.g. ``Protocol[T]``."""
    if isinstance(base, ast.Subscript):
        base = base.value
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return base.attr
    return ""
