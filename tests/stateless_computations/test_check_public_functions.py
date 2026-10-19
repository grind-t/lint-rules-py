from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_multiple_public_functions import (
    ViolationMultiplePublicFunctions,
)
from lint_rules._stateless_computations.check_public_functions import (
    check_public_functions,
)
from lint_rules._stateless_computations.parse_file import parse_file

_TWO_FUNCTIONS = "def f(): ...\ndef g(): ..."
_STATELESS_LAYERS = (
    "_stateless_computations",
    "_stateless_workflows",
    "_stateless_effects",
)


def check(path: str, source: str) -> list[Violation]:
    return check_public_functions(parse_file(SourceFile("src", path, source)))


def test_reports_stateless_module_with_two_public_functions(subtests):
    for layer in _STATELESS_LAYERS:
        path = f"src/pkg/{layer}/a.py"
        with subtests.test(layer):
            assert check(path, _TWO_FUNCTIONS) == [
                ViolationMultiplePublicFunctions(path, functions=("f", "g"))
            ]


def test_passes_stateless_module_with_one_public_function():
    assert check("src/pkg/_stateless_computations/a.py", "def f(): ...") == []


def test_passes_other_layers():
    assert check("src/pkg/_stateful_computations/a.py", _TWO_FUNCTIONS) == []
