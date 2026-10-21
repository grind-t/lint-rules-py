from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_single_method_class import (
    ViolationSingleMethodClass,
)
from lint_rules._stateless_computations.ast_single_method_classes import (
    ast_single_method_classes,
)


def check_single_method_classes(file: ParsedFile) -> list[Violation]:
    return [
        ViolationSingleMethodClass(
            file.path, location, class_name=class_name, method_name=method_name
        )
        for class_name, method_name, location in ast_single_method_classes(file.tree)
    ]
