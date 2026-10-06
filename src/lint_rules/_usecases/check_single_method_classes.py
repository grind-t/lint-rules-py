import ast

from lint_rules._core.single_method_classes import single_method_classes
from lint_rules._core.violation import Violation

MARKER = "# allow-single-method-classes"


def check_single_method_classes(
    path: str, source: str, tree: ast.Module
) -> list[Violation]:
    if MARKER in source:
        return []
    return [
        Violation(
            path,
            f"line {line}: class {cls} has a single method {method}; "
            "use a function, a Callable alias or a Protocol with __call__",
        )
        for cls, method, line in single_method_classes(tree)
    ]
