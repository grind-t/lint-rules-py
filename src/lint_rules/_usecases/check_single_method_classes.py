from lint_rules._core.parsed_file import ParsedFile
from lint_rules._core.single_method_classes import single_method_classes
from lint_rules._core.violation import Violation

_MARKER = "# allow-single-method-classes"


def check_single_method_classes(file: ParsedFile) -> list[Violation]:
    if _MARKER in file.source:
        return []
    return [
        Violation(
            file.path,
            f"class {cls} has a single method {method}; "
            "use a function, a Callable alias or a Protocol with __call__",
            location,
        )
        for cls, method, location in single_method_classes(file.tree)
    ]
