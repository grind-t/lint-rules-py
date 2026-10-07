from lint_rules._core.module_getattr import binds_module_getattr
from lint_rules._core.parsed_file import ParsedFile
from lint_rules._core.violation import Violation


def check_module_getattr(file: ParsedFile) -> list[Violation]:
    if not binds_module_getattr(file.table):
        return []
    message = "module-level __getattr__ makes names dynamic; define them explicitly"
    return [Violation(file.path, message)]
