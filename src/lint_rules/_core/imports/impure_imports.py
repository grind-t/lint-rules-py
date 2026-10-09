import ast
from collections.abc import Callable

from lint_rules._core.imports.from_imports import from_imports
from lint_rules._core.imports.plain_imports import plain_imports
from lint_rules._core.source.source_location import SourceLocation

# Modules that do I/O, each with the names that are safe to import from it.
# A module that is absent here, or whose predicate is always false, has none.
_PURE_NAMES: dict[str, Callable[[str], bool]] = {
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


def impure_imports(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(statement, location)`` of every import of a name that may do I/O.

    Only ``from module import name`` can be told apart by name. A plain
    ``import module`` exposes everything in it, so it is always reported;
    ``from os import path`` is too, since ``os.path`` is not wholly pure.
    """
    found = [
        (f"from {module} import {name}", location)
        for module, name, location in from_imports(tree)
        if module in _PURE_NAMES and not _PURE_NAMES[module](name)
    ]
    found.extend(
        (f"import {module}", location)
        for module, location in plain_imports(tree)
        if module in _PURE_NAMES
    )
    return sorted(found, key=lambda item: item[1])
