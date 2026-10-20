import ast
from collections.abc import Callable

from lint_rules._entities.layer import Layer
from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_too_many_public_names import (
    ViolationTooManyPublicNames,
)
from lint_rules._stateless_computations.ast_public_classes import ast_public_classes
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)
from lint_rules._stateless_computations.layer_of import layer_of

type _Collect = Callable[[ast.Module], list[tuple[str, SourceLocation]]]

_KINDS: tuple[tuple[str, _Collect, Callable[[Layer], int]], ...] = (
    ("classes", ast_public_classes, lambda layer: layer.max_public_classes),
    ("functions", ast_public_functions, lambda layer: layer.max_public_functions),
)


def check_public_counts(file: ParsedFile) -> list[Violation]:
    """Modules of a layer package stay within its public class and function limits."""
    layer = layer_of(file.path)
    if layer is None:
        return []
    violations: list[Violation] = []
    for kind, collect, limit_of in _KINDS:
        found = collect(file.tree)
        limit = limit_of(layer)
        if len(found) > limit:
            violations.append(
                ViolationTooManyPublicNames(
                    file.path,
                    found[limit][1],
                    package=layer.name,
                    limit=limit,
                    kind=kind,
                    names=tuple(name for name, _ in found),
                )
            )
    return violations
