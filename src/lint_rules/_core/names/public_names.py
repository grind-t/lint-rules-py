import ast

from lint_rules._core.source.source_location import SourceLocation


def _targets(node: ast.stmt) -> list[ast.expr]:
    match node:
        case ast.Assign():
            return node.targets
        case ast.AnnAssign() | ast.TypeAlias():
            return [node.target if isinstance(node, ast.AnnAssign) else node.name]
    return []


def _defined(node: ast.stmt) -> list[tuple[str, SourceLocation]]:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        return [(node.name, SourceLocation(node.lineno, node.col_offset + 1))]
    return [
        (target.id, SourceLocation(target.lineno, target.col_offset + 1))
        for target in _targets(node)
        if isinstance(target, ast.Name)
    ]


def public_names(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(name, location)`` of every public top-level function, class or variable.

    Names bound by imports are not included, nor are names starting with ``_``.
    """
    return [
        (name, location)
        for node in tree.body
        for name, location in _defined(node)
        if not name.startswith("_")
    ]
