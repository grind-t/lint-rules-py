import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_base_class_name import ast_base_class_name
from lint_rules._stateless_computations.ast_location import ast_location

# Enums and exceptions: subclasses stay the same kind, so they are exempt too.
_EXEMPT_BASES = {
    "Enum",
    "IntEnum",
    "StrEnum",
    "Flag",
    "IntFlag",
    "ReprEnum",
    "ExceptionGroup",
    "BaseExceptionGroup",
}
_EXCEPTION_SUFFIXES = ("Error", "Exception", "Warning")


def _is_exempt_base(name: str, exempt_classes: set[str]) -> bool:
    return (
        name in _EXEMPT_BASES
        or name in exempt_classes
        or name.endswith(_EXCEPTION_SUFFIXES)
    )


def ast_counted_public_classes(tree: ast.Module) -> list[tuple[str, SourceLocation]]:
    """``(name, location)`` of the public top-level classes that count toward a limit.

    Not counted: ``Protocol`` ports, enums and exceptions; they hold no data
    or state. A subclass of a protocol without ``Protocol`` in its bases is an
    implementation and is counted.
    """
    exempt_classes: set[str] = set()
    found: list[tuple[str, SourceLocation]] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [ast_base_class_name(base) for base in node.bases]
        if any(_is_exempt_base(base, exempt_classes) for base in bases):
            exempt_classes.add(node.name)
        elif "Protocol" in bases:
            continue
        elif not node.name.startswith("_"):
            found.append((node.name, ast_location(node)))
    return found
