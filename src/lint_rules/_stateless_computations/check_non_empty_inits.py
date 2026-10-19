from lint_rules._entities.non_empty_init_violation import NonEmptyInitViolation
from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._stateless_computations.init_files import is_top_level_init
from lint_rules._stateless_computations.package_init import is_package_init


def check_non_empty_inits(file: ParsedFile) -> list[Violation]:
    if not is_package_init(file.path) or is_top_level_init(file.path, file.root):
        return []
    if not file.tree.body:  # comments and blank lines are not in the body
        return []
    return [NonEmptyInitViolation(file.path)]
