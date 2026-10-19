import ast

_FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


def ast_public_functions(tree: ast.Module) -> list[str]:
    """Public top-level functions of a module."""
    return [
        node.name
        for node in tree.body
        if isinstance(node, _FUNCTION_TYPES) and not node.name.startswith("_")
    ]
