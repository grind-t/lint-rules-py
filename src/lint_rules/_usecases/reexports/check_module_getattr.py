from lint_rules._core.reexports.module_getattr import binds_module_getattr
from lint_rules._core.reexports.module_getattr_violation import ModuleGetattrViolation
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile


def check_module_getattr(file: ParsedFile) -> list[Violation]:
    if not binds_module_getattr(file.table):
        return []
    return [ModuleGetattrViolation(file.path)]
