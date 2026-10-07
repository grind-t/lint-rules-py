import ast
from collections.abc import Iterator

from lint_rules._core.bases import base_name
from lint_rules._core.source_location import SourceLocation

_FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
_BLOCK_FIELDS = ("body", "orelse", "finalbody", "handlers", "cases")
_BLOCK_TYPES = (ast.stmt, ast.excepthandler, ast.match_case)


def _statements(tree: ast.Module) -> Iterator[ast.AST]:
    """Every statement block of a module, without descending into expressions.

    Classes can only appear among statements, so this finds the same classes
    as ``ast.walk`` while skipping the bulk of the tree.
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


def _is_filler(stmt: ast.stmt) -> bool:
    """Docstrings, ``...`` and ``pass``: statements that add nothing to a class."""
    if isinstance(stmt, ast.Pass):
        return True
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)


def _single_method(cls: ast.ClassDef) -> str | None:
    """Name of the only method of a stateless class."""
    if cls.decorator_list or cls.keywords:
        return None
    bases = {base_name(base) for base in cls.bases} - {"object"}
    if bases - {"Protocol"}:
        return None
    methods: list[str] = []
    for stmt in cls.body:
        if isinstance(stmt, _FUNCTION_TYPES):
            methods.append(stmt.name)
        elif not _is_filler(stmt):
            return None
    if len(methods) != 1 or methods == ["__init__"]:
        return None
    if "Protocol" in bases and methods == ["__call__"]:
        return None
    return methods[0]


def single_method_classes(tree: ast.Module) -> list[tuple[str, str, SourceLocation]]:
    """``(class, method, location)`` for every class that should be a function.

    A class qualifies when its body is one method other than ``__init__`` and
    nothing else: no decorators, no base classes other than ``Protocol``,
    no class attributes. A ``Protocol`` whose only method is ``__call__`` is
    the recommended replacement and is not reported.
    """
    found = [
        (node.name, method, SourceLocation(node.lineno, node.col_offset + 1))
        for node in _statements(tree)
        if isinstance(node, ast.ClassDef) and (method := _single_method(node))
    ]
    return sorted(found, key=lambda item: item[2])
