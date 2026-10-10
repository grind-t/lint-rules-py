from collections.abc import Callable, Iterable

from lint_rules._core.classes.check_public_classes import check_public_classes
from lint_rules._core.classes.check_single_method_classes import (
    check_single_method_classes,
)
from lint_rules._core.imports.check_impure_imports import (
    check_impure_imports,
)
from lint_rules._core.imports.first_party.check_first_party_module_from_imports import (
    CheckFirstPartyModuleFromImports,
)
from lint_rules._core.imports.first_party.check_plain_first_party_imports import (
    CheckPlainFirstPartyImports,
)
from lint_rules._core.layout.check_crowded_directories import (
    CheckCrowdedDirectories,
)
from lint_rules._core.layout.check_unshared_modules import CheckUnsharedModules
from lint_rules._core.names.check_unimported_public_names import (
    CheckUnimportedPublicNames,
)
from lint_rules._core.reexports.check_module_getattr import check_module_getattr
from lint_rules._core.reexports.check_non_empty_inits import (
    check_non_empty_inits,
)
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_file import SourceFile
from lint_rules._core.stateful_check import StatefulCheck
from lint_rules._core.stateless_check import StatelessCheck

_CHECKS: tuple[StatelessCheck, ...] = (
    check_public_classes,
    check_single_method_classes,
    check_module_getattr,
    check_impure_imports,
    check_non_empty_inits,
)

_STATEFUL_CHECKS: tuple[Callable[[], StatefulCheck], ...] = (
    CheckPlainFirstPartyImports,
    CheckFirstPartyModuleFromImports,
    CheckCrowdedDirectories,
    CheckUnsharedModules,
    CheckUnimportedPublicNames,
)


def check_source_files(source_files: Iterable[SourceFile]) -> list[Violation]:
    """Run every check on each file, parsing it only once.

    Per-file checks report as each file is read; stateful checks start fresh
    on every call and report after the last file.
    """
    stateful = [make() for make in _STATEFUL_CHECKS]
    violations = []
    for source_file in source_files:
        file = ParsedFile(source_file)
        for check in _CHECKS:
            violations.extend(check(file))
        for check in stateful:
            check.visit(file)
    for check in stateful:
        violations.extend(check.finish())
    return violations
