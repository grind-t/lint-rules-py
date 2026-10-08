import ast

from lint_rules._core.shared.statements import statements
from lint_rules._core.source.source_location import SourceLocation


def from_imports(tree: ast.Module) -> list[tuple[str, str, SourceLocation]]:
    """``(module, name, location)`` of every ``from module import name``.

    Each name of ``from a import b, c`` is its own entry, located at its alias.
    Relative imports, ``import *`` and plain ``import module`` are not included.
    """
    found = [
        (node.module, alias.name, SourceLocation(alias.lineno, alias.col_offset + 1))
        for node in statements(tree)
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module
        for alias in node.names
        if alias.name != "*"
    ]
    return sorted(found, key=lambda item: item[2])
