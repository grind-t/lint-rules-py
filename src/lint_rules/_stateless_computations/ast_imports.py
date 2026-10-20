import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_location import ast_location
from lint_rules._stateless_computations.ast_statements import ast_statements


def ast_imports(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(module, location)`` of every ``import module`` anywhere in the module.

    Each name of ``import a, b`` is its own entry, located at its alias.
    ``from module import name`` is not included.
    """
    found = [
        (alias.name, ast_location(alias))
        for node in ast_statements(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    ]
    return sorted(found, key=lambda item: item[1])
