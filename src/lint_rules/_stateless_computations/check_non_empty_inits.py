from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_non_empty_init import ViolationNonEmptyInit
from lint_rules._stateless_computations.is_package_init import is_package_init
from lint_rules._stateless_computations.is_top_level_init import is_top_level_init


def check_non_empty_inits(file: ParsedFile) -> list[Violation]:
    if not is_package_init(file.path) or is_top_level_init(file.path, file.root):
        return []
    if not file.tree.body:  # comments and blank lines are not in the body
        return []
    return [ViolationNonEmptyInit(file.path)]
