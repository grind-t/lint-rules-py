from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_module_name_mismatch import (
    ViolationModuleNameMismatch,
)
from lint_rules._stateless_computations.ast_public_names import ast_public_names


def _normalized(name: str) -> str:
    """``parsed_file`` and ``ParsedFile`` both become ``parsedfile``."""
    return name.replace("_", "").lower()


def check_module_names(file: ParsedFile) -> list[Violation]:
    """The module is named after one of its public names.

    Case and underscores are ignored, so ``parsed_file.py`` matches
    ``ParsedFile``. Modules without public names and dunder modules such
    as ``__init__.py`` are skipped.
    """
    stem = file.path.rpartition("/")[2].removesuffix(".py")
    if stem.startswith("__"):
        return []
    names = tuple(name for name, _ in ast_public_names(file.tree))
    if not names or _normalized(stem) in {_normalized(name) for name in names}:
        return []
    return [ViolationModuleNameMismatch(file.path, names=names)]
