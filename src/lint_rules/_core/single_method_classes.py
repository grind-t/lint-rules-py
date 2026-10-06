import ast

from lint_rules._core.bases import base_name

FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


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
        if isinstance(stmt, FUNCTION_TYPES):
            methods.append(stmt.name)
        elif not _is_filler(stmt):
            return None
    if len(methods) != 1 or methods == ["__init__"]:
        return None
    if "Protocol" in bases and methods == ["__call__"]:
        return None
    return methods[0]


def single_method_classes(source: str) -> list[tuple[str, str, int]]:
    """``(class, method, line)`` for every class that should be a function.

    A class qualifies when its body is one method other than ``__init__`` and
    nothing else: no decorators, no base classes other than ``Protocol``,
    no class attributes. A ``Protocol`` whose only method is ``__call__`` is
    the recommended replacement and is not reported.
    """
    return [
        (node.name, method, node.lineno)
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.ClassDef) and (method := _single_method(node))
    ]
