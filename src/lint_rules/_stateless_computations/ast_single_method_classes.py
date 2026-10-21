import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_base_class_name import ast_base_class_name
from lint_rules._stateless_computations.ast_location import ast_location
from lint_rules._stateless_computations.ast_statements import ast_statements


def _is_filler(stmt: ast.stmt) -> bool:
    """Docstrings, ``...`` and ``pass``: statements that add nothing to a class."""
    if isinstance(stmt, ast.Pass):
        return True
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)


def _single_method_name(node: ast.ClassDef) -> str | None:
    """Name of the only method of a stateless class."""
    if node.decorator_list or node.keywords:
        return None
    bases = {ast_base_class_name(base) for base in node.bases} - {"object"}
    if bases - {"Protocol"}:
        return None
    methods: list[str] = []
    for stmt in node.body:
        if isinstance(stmt, ast.FunctionDef | ast.AsyncFunctionDef):
            methods.append(stmt.name)
        elif not _is_filler(stmt):
            return None
    if len(methods) != 1 or methods == ["__init__"]:
        return None
    if "Protocol" in bases and methods == ["__call__"]:
        return None
    return methods[0]


def ast_single_method_classes(
    tree: ast.Module,
) -> list[tuple[str, str, SourceLocation]]:
    """``(class, method, location)`` for every class that should be a function.

    A class qualifies when its body is one method other than ``__init__`` and
    nothing else: no decorators, no base classes other than ``Protocol``,
    no class attributes. A ``Protocol`` whose only method is ``__call__`` is
    the recommended replacement and is not reported.
    """
    return [
        (node.name, method, ast_location(node))
        for node in ast_statements(tree)
        if isinstance(node, ast.ClassDef) and (method := _single_method_name(node))
    ]
