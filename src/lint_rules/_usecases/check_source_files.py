import ast
from collections.abc import Callable, Iterable
from typing import Protocol

from lint_rules._core.violation import Violation
from lint_rules._ports.source_files import ReadSourceFiles
from lint_rules._usecases.check_public_classes import check_public_classes
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)
from lint_rules._usecases.check_unused_public_names import (
    CheckUnusedPublicNames,
)

type Check = Callable[[str, str, ast.Module], list[Violation]]


class StatefulCheck(Protocol):
    """A check that needs every file before it can report anything."""

    def visit(self, path: str, source: str, tree: ast.Module) -> None: ...

    def finish(self) -> list[Violation]: ...


_CHECKS: tuple[Check, ...] = (check_public_classes, check_single_method_classes)

# Factories, not instances: every run starts with fresh state.
_STATEFUL_CHECKS: tuple[Callable[[], StatefulCheck], ...] = (CheckUnusedPublicNames,)


def check_source_files(
    read_files: ReadSourceFiles, roots: Iterable[str]
) -> list[Violation]:
    """Run every check on each file, parsing it only once."""
    stateful = [make() for make in _STATEFUL_CHECKS]
    violations = []
    for path, source in read_files(roots):
        tree = ast.parse(source)
        for check in _CHECKS:
            violations.extend(check(path, source, tree))
        for check in stateful:
            check.visit(path, source, tree)
    for check in stateful:
        violations.extend(check.finish())
    return violations
