import ast
from collections.abc import Iterator

_BLOCK_FIELDS = ("body", "orelse", "finalbody", "handlers", "cases")
_BLOCK_TYPES = (ast.stmt, ast.excepthandler, ast.match_case)


def statements(tree: ast.Module) -> Iterator[ast.AST]:
    """Every statement block of a module, without descending into expressions.

    Classes and imports can only appear among statements, so this finds the
    same ones as ``ast.walk`` while skipping the bulk of the tree.
    """
    stack: list[ast.AST] = [tree]
    while stack:
        node = stack.pop()
        yield node
        for field in _BLOCK_FIELDS:
            block = getattr(node, field, None)
            if isinstance(block, list):
                stack.extend(
                    child for child in block if isinstance(child, _BLOCK_TYPES)
                )
