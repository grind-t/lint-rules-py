from collections.abc import Callable, Iterable, Iterator

from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.violation import Violation
from lint_rules._stateful_computations.check_first_party_module_imports import (
    CheckFirstPartyModuleImports,
)
from lint_rules._stateful_computations.check_first_party_module_imports_from import (
    CheckFirstPartyModuleImportsFrom,
)
from lint_rules._stateful_computations.check_unimported_public_names import (
    CheckUnimportedPublicNames,
)
from lint_rules._stateful_computations.stateful_check import StatefulCheck
from lint_rules._stateless_computations.check_entities_public_functions import (
    check_entities_public_functions,
)
from lint_rules._stateless_computations.check_impure_imports import (
    check_impure_imports,
)
from lint_rules._stateless_computations.check_module_getattr import check_module_getattr
from lint_rules._stateless_computations.check_non_empty_inits import (
    check_non_empty_inits,
)
from lint_rules._stateless_computations.check_public_classes import check_public_classes
from lint_rules._stateless_computations.check_single_method_classes import (
    check_single_method_classes,
)
from lint_rules._stateless_computations.check_stateful_public_functions import (
    check_stateful_public_functions,
)
from lint_rules._stateless_computations.check_stateless_public_classes import (
    check_stateless_public_classes,
)
from lint_rules._stateless_computations.check_stateless_public_functions import (
    check_stateless_public_functions,
)
from lint_rules._stateless_computations.parse_file import parse_file
from lint_rules._stateless_computations.stateless_check import StatelessCheck

_CHECKS: tuple[StatelessCheck, ...] = (
    check_public_classes,
    check_stateless_public_functions,
    check_stateless_public_classes,
    check_entities_public_functions,
    check_stateful_public_functions,
    check_single_method_classes,
    check_module_getattr,
    check_impure_imports,
    check_non_empty_inits,
)

_STATEFUL_CHECKS: tuple[Callable[[], StatefulCheck], ...] = (
    CheckFirstPartyModuleImports,
    CheckFirstPartyModuleImportsFrom,
    CheckUnimportedPublicNames,
)


def _violations(source_files: Iterable[SourceFile]) -> Iterator[Violation]:
    stateful = [make() for make in _STATEFUL_CHECKS]
    for source_file in source_files:
        file = parse_file(source_file)
        for check in _CHECKS:
            yield from check(file)
        for check in stateful:
            check.visit(file)
    for check in stateful:
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
