import ast

from lint_rules._core.shared.statements import statements


def imported_modules(tree: ast.Module) -> set[str]:
    """Every module an absolute import anywhere in the module may refer to.

    ``from a import b`` gives both ``a`` and ``a.b``, since ``b`` may be a
    submodule; relative imports are left out.
    """
    found: set[str] = set()
    for node in statements(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.add(node.module)
            found.update(
                f"{node.module}.{alias.name}"
                for alias in node.names
                if alias.name != "*"
            )
    return found
