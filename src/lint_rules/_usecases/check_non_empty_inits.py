from lint_rules._core.reexports.init_files import is_top_level_init
from lint_rules._core.reexports.non_empty_init_violation import NonEmptyInitViolation
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile

_PACKAGE_INIT = "__init__.py"


def check_non_empty_inits(file: ParsedFile) -> list[Violation]:
    is_init = file.path.rpartition("/")[2] == _PACKAGE_INIT
    if not is_init or is_top_level_init(file.path, file.root):
        return []
    if not file.tree.body:  # comments and blank lines are not in the body
        return []
    return [NonEmptyInitViolation(file.path)]
