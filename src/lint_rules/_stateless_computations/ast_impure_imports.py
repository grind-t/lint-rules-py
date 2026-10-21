import ast
from collections.abc import Callable

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_from_imports import ast_from_imports
from lint_rules._stateless_computations.ast_imports import ast_imports

# Modules that do I/O, each with a test for the names that are safe to import
# from it. Modules absent here do no I/O, so any of their names is safe.
_IS_PURE_NAME_BY_IO_MODULE: dict[str, Callable[[str], bool]] = {
    "io": frozenset(
        {
            "BytesIO",
            "StringIO",
            "IOBase",
            "RawIOBase",
            "BufferedIOBase",
            "TextIOBase",
            "UnsupportedOperation",
        }
    ).__contains__,
    "os": frozenset(
        {"PathLike", "fspath", "fsencode", "fsdecode", "sep", "extsep", "pathsep"}
    ).__contains__,
    "os.path": frozenset(
        {
            "join",
            "split",
            "splitext",
            "basename",
            "dirname",
            "normpath",
            "isabs",
            "commonpath",
            "commonprefix",
        }
    ).__contains__,
    "pathlib": lambda name: name.startswith("Pure"),
    "socket": lambda _name: False,
    "subprocess": lambda _name: False,
}


def ast_impure_imports(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(import_text, location)`` of every import of a name that may do I/O.

    Only ``from module import name`` can be told apart by name. A plain
    ``import module`` exposes everything in it, so it is always reported;
    ``from os import path`` is too, since ``os.path`` is not wholly pure.
    """
    found = [
        (f"from {module} import {name}", location)
        for module, name, location in ast_from_imports(tree)
        if module in _IS_PURE_NAME_BY_IO_MODULE
        and not _IS_PURE_NAME_BY_IO_MODULE[module](name)
    ]
    found.extend(
        (f"import {module}", location)
        for module, location in ast_imports(tree)
        if module in _IS_PURE_NAME_BY_IO_MODULE
    )
    return sorted(found, key=lambda item: item[1])
