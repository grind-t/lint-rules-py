from collections.abc import Callable
from typing import Protocol, runtime_checkable

from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._ports.source_files import ReadSourceFiles
from lint_rules._usecases.check_crowded_directories import CheckCrowdedDirectories
from lint_rules._usecases.check_first_party_module_from_imports import (
    CheckFirstPartyModuleFromImports,
)
from lint_rules._usecases.check_impure_imports import (
    check_impure_imports,
)
from lint_rules._usecases.check_module_getattr import check_module_getattr
from lint_rules._usecases.check_plain_first_party_imports import (
    CheckPlainFirstPartyImports,
)
from lint_rules._usecases.check_public_classes import check_public_classes
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)
from lint_rules._usecases.check_unshared_modules import CheckUnsharedModules

type Check = Callable[[ParsedFile], list[Violation]]


@runtime_checkable
class StatefulCheck(Protocol):
    """A check that needs every file before it can report, e.g. across files."""

    def visit(self, file: ParsedFile) -> None:
        """Collect what the check needs from one file."""
        ...

    def finish(self) -> list[Violation]:
        """Report once every file has been visited."""
        ...


_CHECKS: tuple[Check, ...] = (
    check_public_classes,
    check_single_method_classes,
    check_module_getattr,
    check_impure_imports,
)

_STATEFUL_CHECKS: tuple[Callable[[str], StatefulCheck], ...] = (
    CheckPlainFirstPartyImports,
    CheckFirstPartyModuleFromImports,
    lambda _root: CheckCrowdedDirectories(),
    CheckUnsharedModules,
)


def check_source_files(read_files: ReadSourceFiles, root: str) -> list[Violation]:
    """Run every check on each file, parsing it only once.

    Per-file checks report as each file is read; stateful checks start fresh
    on every call and report after the last file.
    """
    stateful = [make(root) for make in _STATEFUL_CHECKS]
    violations = []
    for source_file in read_files(root):
        file = ParsedFile(source_file)
        for check in _CHECKS:
            violations.extend(check(file))
        for check in stateful:
            check.visit(file)
    for check in stateful:
        violations.extend(check.finish())
    return violations
