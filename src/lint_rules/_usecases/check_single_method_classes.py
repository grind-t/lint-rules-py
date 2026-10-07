import ast

from lint_rules._core.single_method_classes import single_method_classes
from lint_rules._core.violation import Violation

_MARKER = "# allow-single-method-classes"


def check_single_method_classes(
    path: str, source: str, tree: ast.Module
) -> list[Violation]:
    if _MARKER in source:
        return []
    return [
        Violation(
            path,
            f"class {cls} has a single method {method}; "
            "use a function, a Callable alias or a Protocol with __call__",
            location,
        )
        for cls, method, location in single_method_classes(tree)
    ]
