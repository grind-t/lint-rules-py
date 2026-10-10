from lint_rules._core.reexports.init_files import is_top_level_init
from lint_rules._core.reexports.non_empty_init_violation import NonEmptyInitViolation
from lint_rules._core.shared.package_init import is_package_init
from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile


def check_non_empty_inits(file: ParsedFile) -> list[Violation]:
    if not is_package_init(file.path) or is_top_level_init(file.path, file.root):
        return []
    if not file.tree.body:  # comments and blank lines are not in the body
        return []
    return [NonEmptyInitViolation(file.path)]
