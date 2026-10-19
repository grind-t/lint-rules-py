import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_base_class_name import ast_base_class_name


def ast_public_non_protocol_classes(
    tree: ast.Module,
) -> list[tuple[str, SourceLocation]]:
    """``(class, location)`` of every public top-level class except Protocols."""
    return [
        (node.name, SourceLocation(node.lineno, node.col_offset + 1))
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and not node.name.startswith("_")
        and "Protocol" not in {ast_base_class_name(base) for base in node.bases}
    ]
