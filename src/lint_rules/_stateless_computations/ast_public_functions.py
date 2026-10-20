import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_location import ast_location


def ast_public_functions(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(name, location)`` of every public top-level function of a module."""
    return [
        (node.name, ast_location(node))
        for node in tree.body
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
        and not node.name.startswith("_")
    ]
