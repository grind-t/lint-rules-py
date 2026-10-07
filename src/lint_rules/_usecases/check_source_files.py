from collections.abc import Callable, Iterable

from lint_rules._core.parsed_file import ParsedFile
from lint_rules._core.violation import Violation
from lint_rules._ports.source_files import ReadSourceFiles
from lint_rules._usecases.check_module_getattr import check_module_getattr
from lint_rules._usecases.check_public_classes import check_public_classes
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)

type Check = Callable[[ParsedFile], list[Violation]]

_CHECKS: tuple[Check, ...] = (
    check_public_classes,
    check_single_method_classes,
    check_module_getattr,
)


def check_source_files(
    read_files: ReadSourceFiles, roots: Iterable[str]
) -> list[Violation]:
    """Run every check on each file, parsing it only once."""
    violations = []
    for path, source in read_files(roots):
        file = ParsedFile(path, source)
        for check in _CHECKS:
            violations.extend(check(file))
    return violations
