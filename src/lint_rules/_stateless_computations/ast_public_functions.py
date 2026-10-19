import ast

from lint_rules._entities.source_location import SourceLocation

_FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


def ast_public_functions(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(name, location)`` of every public top-level function of a module."""
    return [
        (node.name, SourceLocation(node.lineno, node.col_offset + 1))
        for node in tree.body
        if isinstance(node, _FUNCTION_TYPES) and not node.name.startswith("_")
    ]
