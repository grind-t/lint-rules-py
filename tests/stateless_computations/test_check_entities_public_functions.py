from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_entities_public_function import (
    ViolationEntitiesPublicFunction,
)
from lint_rules._stateless_computations.check_entities_public_functions import (
    check_entities_public_functions,
)
from lint_rules._stateless_computations.parse_file import parse_file


def check(path: str, source: str) -> list[Violation]:
    return check_entities_public_functions(parse_file(SourceFile("src", path, source)))


def test_reports_public_function_in_entities():
    path = "src/pkg/_entities/a.py"
    assert check(path, "def f(): ...") == [
        ViolationEntitiesPublicFunction(path, SourceLocation(1, 1), name="f")
    ]


def test_passes_private_function_in_entities():
    assert check("src/pkg/_entities/a.py", "def _f(): ...") == []


def test_passes_other_layers():
    assert check("src/pkg/_stateless_computations/a.py", "def f(): ...") == []
