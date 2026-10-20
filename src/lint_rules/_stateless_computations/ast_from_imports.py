import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_location import ast_location
from lint_rules._stateless_computations.ast_statements import ast_statements


def ast_from_imports(tree: ast.Module) -> list[tuple[str, str, SourceLocation]]:
    """``(module, name, location)`` of every ``from module import name``.

    Each name of ``from a import b, c`` is its own entry, located at its alias.
    Relative imports, ``import *`` and plain ``import module`` are not included.
    """
    found = [
        (node.module, alias.name, ast_location(alias))
        for node in ast_statements(tree)
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module
        for alias in node.names
        if alias.name != "*"
    ]
    return sorted(found, key=lambda item: item[2])
