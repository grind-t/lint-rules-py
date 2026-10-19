from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_stateless_public_class import (
    ViolationStatelessPublicClass,
)
from lint_rules._stateless_computations.check_stateless_public_classes import (
    check_stateless_public_classes,
)
from lint_rules._stateless_computations.parse_file import parse_file

_STATELESS_LAYERS = (
    "_stateless_computations",
    "_stateless_workflows",
    "_stateless_effects",
)


def check(path: str, source: str) -> list[Violation]:
    return check_stateless_public_classes(parse_file(SourceFile("src", path, source)))


def test_reports_public_class_in_stateless_module(subtests):
    for layer in _STATELESS_LAYERS:
        path = f"src/pkg/{layer}/a.py"
        with subtests.test(layer):
            assert check(path, "class A: ...") == [
                ViolationStatelessPublicClass(path, SourceLocation(1, 1), name="A")
            ]


def test_passes_protocol_in_stateless_module():
    assert check("src/pkg/_stateless_workflows/a.py", "class P(Protocol): ...") == []


def test_passes_other_layers():
    assert check("src/pkg/_entities/a.py", "class A: ...") == []
