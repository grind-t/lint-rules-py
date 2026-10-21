from collections.abc import Callable, Iterable, Iterator

from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.violation import Violation
from lint_rules._stateful_computations.check_first_party_module_imports import (
    CheckFirstPartyModuleImports,
)
from lint_rules._stateful_computations.check_unimported_public_names import (
    CheckUnimportedPublicNames,
)
from lint_rules._stateful_computations.stateful_check import StatefulCheck
from lint_rules._stateless_computations.check_impure_imports import (
    check_impure_imports,
)
from lint_rules._stateless_computations.check_module_getattr import check_module_getattr
from lint_rules._stateless_computations.check_module_name_mismatch import (
    check_module_name_mismatch,
)
from lint_rules._stateless_computations.check_non_empty_inits import (
    check_non_empty_inits,
)
from lint_rules._stateless_computations.check_single_method_classes import (
    check_single_method_classes,
)
from lint_rules._stateless_computations.check_too_many_public_definitions import (
    check_too_many_public_definitions,
)
from lint_rules._stateless_computations.parse_file import parse_file
from lint_rules._stateless_computations.stateless_check import StatelessCheck

_STATELESS_CHECKS: tuple[StatelessCheck, ...] = (
    check_too_many_public_definitions,
    check_single_method_classes,
    check_module_getattr,
    check_module_name_mismatch,
    check_impure_imports,
    check_non_empty_inits,
)

_STATEFUL_CHECK_TYPES: tuple[Callable[[], StatefulCheck], ...] = (
    CheckFirstPartyModuleImports,
    CheckUnimportedPublicNames,
)


def _violations(source_files: Iterable[SourceFile]) -> Iterator[Violation]:
    stateful_checks = [check_type() for check_type in _STATEFUL_CHECK_TYPES]
    for source_file in source_files:
        file = parse_file(source_file)
        for check in _STATELESS_CHECKS:
            yield from check(file)
        for check in stateful_checks:
            check.visit(file)
    for check in stateful_checks:
        yield from check.finish()


def lint(
    source_files: Iterable[SourceFile], report: Callable[[Violation], None]
) -> int:
    """Run every check on each file, parsing it only once; return the violation count.

    Per-file checks report as each file is read; stateful checks start fresh
    on every call and report after the last file.
    """
    count = 0
    for violation in _violations(source_files):
        report(violation)
        count += 1
    return count
