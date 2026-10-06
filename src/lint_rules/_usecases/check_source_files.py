import ast
from collections.abc import Callable, Iterable

from lint_rules._core.violation import Violation
from lint_rules._ports.source_files import ReadSourceFiles
from lint_rules._usecases.check_public_classes import check_public_classes
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)

type Check = Callable[[str, str, ast.Module], list[Violation]]

CHECKS: tuple[Check, ...] = (check_public_classes, check_single_method_classes)


def check_source_files(
    read_files: ReadSourceFiles, roots: Iterable[str]
) -> list[Violation]:
    """Run every check on each file, parsing it only once."""
    violations = []
    for path, source in read_files(roots):
        tree = ast.parse(source)
        for check in CHECKS:
            violations.extend(check(path, source, tree))
    return violations
