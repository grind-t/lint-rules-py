import ast

from lint_rules._entities.source_location import SourceLocation


def ast_location(node: ast.stmt | ast.expr | ast.alias) -> SourceLocation:
    """Where the node starts; AST columns are 0-based, ours are 1-based."""
    return SourceLocation(node.lineno, node.col_offset + 1)
