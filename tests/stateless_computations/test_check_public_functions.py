from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_too_many_public_functions import (
    ViolationTooManyPublicFunctions,
)
from lint_rules._stateless_computations.check_public_functions import (
    check_public_functions,
)
from lint_rules._stateless_computations.parse_file import parse_file

_LIMITS = {
    "_entities": 0,
    "_stateless_computations": 1,
    "_stateless_workflows": 1,
    "_stateless_effects": 1,
    "_stateful_computations": 0,
    "_stateful_workflows": 0,
    "_stateful_effects": 0,
}


def check(path: str, source: str) -> list[Violation]:
    return check_public_functions(parse_file(SourceFile("src", path, source)))


def functions(count: int) -> str:
    return "".join(f"def f{i}(): ...\n" for i in range(count))


def test_reports_module_over_package_limit(subtests):
    for package, limit in _LIMITS.items():
        path = f"src/pkg/{package}/a.py"
        names = tuple(f"f{i}" for i in range(limit + 1))
        with subtests.test(package):
            assert check(path, functions(limit + 1)) == [
                ViolationTooManyPublicFunctions(
                    path,
                    SourceLocation(limit + 1, 1),
                    package=package,
                    limit=limit,
                    functions=names,
                )
            ]


def test_passes_module_at_package_limit(subtests):
    for package, limit in _LIMITS.items():
        with subtests.test(package):
            assert check(f"src/pkg/{package}/a.py", functions(limit)) == []


def test_ignores_private_functions():
    assert check("src/pkg/_entities/a.py", "def _f(): ...") == []


def test_passes_modules_outside_layer_packages():
    assert check("src/pkg/a.py", functions(2)) == []
