from lint_rules._core.classes.single_method_classes import single_method_classes
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.violation import Violation
from lint_rules._core.violations.single_method_class import SingleMethodClassViolation

_MARKER = "# allow-single-method-classes"


def check_single_method_classes(file: ParsedFile) -> list[Violation]:
    if _MARKER in file.source:
        return []
    return [
        SingleMethodClassViolation(file.path, location, cls=cls, method=method)
        for cls, method, location in single_method_classes(file.tree)
    ]
