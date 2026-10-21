import ast
from collections.abc import Callable

from lint_rules._entities.layer import Layer
from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_too_many_public_definitions import (
    ViolationTooManyPublicDefinitions,
)
from lint_rules._stateless_computations.ast_counted_public_classes import (
    ast_counted_public_classes,
)
from lint_rules._stateless_computations.ast_public_functions import (
    ast_public_functions,
)
from lint_rules._stateless_computations.layer_of import layer_of

type _CollectDefinitions = Callable[[ast.Module], list[tuple[str, SourceLocation]]]

_KIND_LIMITS: tuple[tuple[str, _CollectDefinitions, Callable[[Layer], int]], ...] = (
    ("classes", ast_counted_public_classes, lambda layer: layer.public_class_limit),
    ("functions", ast_public_functions, lambda layer: layer.public_function_limit),
)


def check_too_many_public_definitions(file: ParsedFile) -> list[Violation]:
    """Modules of a layer package stay within its public class and function limits."""
    layer = layer_of(file.path)
    if layer is None:
        return []
    violations: list[Violation] = []
    for kind, collect, limit_of in _KIND_LIMITS:
        definitions = collect(file.tree)
        limit = limit_of(layer)
        if len(definitions) > limit:
            _, first_excess_location = definitions[limit]
            violations.append(
                ViolationTooManyPublicDefinitions(
                    file.path,
                    first_excess_location,
                    layer=layer.name,
                    limit=limit,
                    kind=kind,
                    names=tuple(name for name, _ in definitions),
                )
            )
    return violations
