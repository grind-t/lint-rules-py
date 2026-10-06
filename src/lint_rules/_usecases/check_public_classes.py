import ast

from lint_rules._core.public_classes import public_classes
from lint_rules._core.violation import Violation

_MARKER = "# allow-multiple-public-classes"


def check_public_classes(path: str, source: str, tree: ast.Module) -> list[Violation]:
    if _MARKER in source:
        return []
    classes = public_classes(tree)
    if len(classes) <= 1:
        return []
    message = (
        f"{len(classes)} public classes ({', '.join(classes)}); "
        "split them into separate modules"
    )
    return [Violation(path, message)]
