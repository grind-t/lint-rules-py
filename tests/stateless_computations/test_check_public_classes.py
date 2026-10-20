from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_too_many_public_classes import (
    ViolationTooManyPublicClasses,
)
from lint_rules._stateless_computations.check_public_classes import check_public_classes
from lint_rules._stateless_computations.parse_file import parse_file

_LIMITS = {
    "_entities": 1,
    "_stateless_computations": 0,
    "_stateless_workflows": 0,
    "_stateless_effects": 0,
    "_stateful_computations": 1,
    "_stateful_workflows": 1,
    "_stateful_effects": 1,
}


def check(path: str, source: str) -> list[Violation]:
    return check_public_classes(parse_file(SourceFile("src", path, source)))


def classes(count: int) -> str:
    return "".join(f"class C{i}: ...\n" for i in range(count))


def test_reports_module_over_package_limit(subtests):
    for package, limit in _LIMITS.items():
        path = f"src/pkg/{package}/a.py"
        names = tuple(f"C{i}" for i in range(limit + 1))
        with subtests.test(package):
            assert check(path, classes(limit + 1)) == [
                ViolationTooManyPublicClasses(
                    path,
                    SourceLocation(limit + 1, 1),
                    package=package,
                    limit=limit,
                    classes=names,
                )
            ]


def test_passes_module_at_package_limit(subtests):
    for package, limit in _LIMITS.items():
        with subtests.test(package):
            assert check(f"src/pkg/{package}/a.py", classes(limit)) == []


def test_ignores_non_class_definitions():
    source = "class E(Exception): ...\nclass K(Enum): ...\nclass P(Protocol): ..."
    assert check("src/pkg/_stateless_workflows/a.py", source) == []


def test_passes_modules_outside_layer_packages():
    assert check("src/pkg/a.py", classes(2)) == []
