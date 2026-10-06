from collections.abc import Iterable

from lint_rules._core.single_method_classes import single_method_classes
from lint_rules._core.violation import Violation
from lint_rules._ports.source_files import ReadSourceFiles

MARKER = "# allow-single-method-classes"


def check_single_method_classes(
    read_files: ReadSourceFiles, roots: Iterable[str]
) -> list[Violation]:
    violations = []
    for path, source in read_files(roots):
        if MARKER in source:
            continue
        for cls, method, line in single_method_classes(source):
            message = (
                f"line {line}: class {cls} has a single method {method}; "
                "use a function, a Callable alias or a Protocol with __call__"
            )
            violations.append(Violation(path, message))
    return violations
