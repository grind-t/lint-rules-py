import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_location import ast_location


def _targets(node: ast.stmt) -> list[ast.expr]:
    match node:
        case ast.Assign():
            return node.targets
        case ast.AnnAssign() | ast.TypeAlias():
            return [node.target if isinstance(node, ast.AnnAssign) else node.name]
    return []


def _bound_names(node: ast.stmt) -> list[tuple[str, SourceLocation]]:
    if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
        return [(node.name, ast_location(node))]
    return [
        (target.id, ast_location(target))
        for target in _targets(node)
        if isinstance(target, ast.Name)
    ]


def ast_public_names(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(name, location)`` of every public top-level function, class or variable.

    Names bound by imports are not included, nor are names starting with ``_``.
    """
    return [
        (name, location)
        for node in tree.body
        for name, location in _bound_names(node)
        if not name.startswith("_")
    ]
