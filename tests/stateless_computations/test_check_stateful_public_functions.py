from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_stateful_public_function import (
    ViolationStatefulPublicFunction,
)
from lint_rules._stateless_computations.check_stateful_public_functions import (
    check_stateful_public_functions,
)
from lint_rules._stateless_computations.parse_file import parse_file

_STATEFUL_LAYERS = (
    "_stateful_computations",
    "_stateful_workflows",
    "_stateful_effects",
)


def check(path: str, source: str) -> list[Violation]:
    return check_stateful_public_functions(parse_file(SourceFile("src", path, source)))


def test_reports_public_function_in_stateful_module(subtests):
    for layer in _STATEFUL_LAYERS:
        path = f"src/pkg/{layer}/a.py"
        with subtests.test(layer):
            assert check(path, "def f(): ...") == [
                ViolationStatefulPublicFunction(path, SourceLocation(1, 1), name="f")
            ]


def test_passes_private_function_in_stateful_module():
    assert check("src/pkg/_stateful_computations/a.py", "def _f(): ...") == []


def test_passes_other_layers():
    assert check("src/pkg/_stateless_computations/a.py", "def f(): ...") == []
