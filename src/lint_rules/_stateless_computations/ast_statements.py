import ast
from collections.abc import Iterator

# In the order they appear in the source, e.g. try: body, except, else, finally.
_BLOCK_FIELDS = ("body", "handlers", "orelse", "finalbody", "cases")
_BLOCK_TYPES = (ast.stmt, ast.excepthandler, ast.match_case)


def ast_statements(tree: ast.Module) -> Iterator[ast.AST]:
    """Every statement block of a module in source order, skipping expressions.

    Classes and imports can only appear among statements, so this finds the
    same ones as ``ast.walk`` while skipping the bulk of the tree.
    """
    stack: list[ast.AST] = [tree]
    while stack:
        node = stack.pop()
        yield node
        children = [
            child
            for field in _BLOCK_FIELDS
            if isinstance(block := getattr(node, field, None), list)
            for child in block
            if isinstance(child, _BLOCK_TYPES)
        ]
        stack.extend(reversed(children))
