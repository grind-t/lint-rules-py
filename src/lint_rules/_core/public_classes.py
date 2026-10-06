import ast

from lint_rules._core.bases import base_name

ENUM_BASES = {"Enum", "IntEnum", "StrEnum", "Flag", "IntFlag"}
EXCEPTION_SUFFIXES = ("Error", "Exception", "Warning")


def _is_exempt(cls: ast.ClassDef, exempt: set[str]) -> bool:
    names = [base_name(base) for base in cls.bases]
    return any(
        n in ENUM_BASES or n in exempt or n.endswith(EXCEPTION_SUFFIXES) for n in names
    )


def public_classes(tree: ast.Module) -> list[str]:
    """Public top-level classes of a module, excluding exceptions and enums."""
    exempt: set[str] = set()
    found: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        if _is_exempt(node, exempt):
            exempt.add(node.name)
        elif not node.name.startswith("_"):
            found.append(node.name)
    return found
