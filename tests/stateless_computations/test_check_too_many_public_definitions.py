from lint_rules._entities.source_file import SourceFile
from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_too_many_public_definitions import (
    ViolationTooManyPublicDefinitions,
)
from lint_rules._stateless_computations.check_too_many_public_definitions import (
    check_too_many_public_definitions,
)
from lint_rules._stateless_computations.parse_file import parse_file

# (class limit, function limit) per layer.
_LIMITS = {
    "_entities": (1, 0),
    "_stateless_computations": (0, 1),
    "_stateless_workflows": (0, 1),
    "_stateless_effects": (0, 1),
    "_stateful_computations": (1, 0),
    "_stateful_workflows": (1, 0),
    "_stateful_effects": (1, 0),
}


def check(path: str, source: str) -> list[Violation]:
    return check_too_many_public_definitions(
        parse_file(SourceFile(root="src", path=path, source=source))
    )


def classes(count: int) -> str:
    return "".join(f"class C{i}: ...\n" for i in range(count))


def functions(count: int) -> str:
    return "".join(f"def f{i}(): ...\n" for i in range(count))


def test_reports_module_over_layer_limit(subtests):
    for layer, (class_limit, function_limit) in _LIMITS.items():
        path = f"src/pkg/{layer}/a.py"
        kinds = [
            ("classes", "C", class_limit, classes),
            ("functions", "f", function_limit, functions),
        ]
        for kind, prefix, limit, define in kinds:
            names = tuple(f"{prefix}{i}" for i in range(limit + 1))
            with subtests.test(f"{kind} in {layer}"):
                assert check(path, define(limit + 1)) == [
                    ViolationTooManyPublicDefinitions(
                        path,
                        SourceLocation(limit + 1, 1),
                        layer=layer,
                        limit=limit,
                        kind=kind,
                        names=names,
                    )
                ]


def test_passes_module_at_layer_limit(subtests):
    for layer, (class_limit, function_limit) in _LIMITS.items():
        with subtests.test(layer):
            source = classes(class_limit) + functions(function_limit)
            assert check(f"src/pkg/{layer}/a.py", source) == []


def test_reports_both_kinds_over_limit():
    path = "src/pkg/_entities/a.py"
    assert check(path, classes(2) + "def f(): ...\n") == [
        ViolationTooManyPublicDefinitions(
            path,
            SourceLocation(2, 1),
            layer="_entities",
            limit=1,
            kind="classes",
            names=("C0", "C1"),
        ),
        ViolationTooManyPublicDefinitions(
            path,
            SourceLocation(3, 1),
            layer="_entities",
            limit=0,
            kind="functions",
            names=("f",),
        ),
    ]


def test_ignores_non_class_definitions():
    source = "class E(Exception): ...\nclass K(Enum): ...\nclass P(Protocol): ..."
    assert check("src/pkg/_stateless_workflows/a.py", source) == []


def test_ignores_private_functions():
    assert check("src/pkg/_entities/a.py", "def _f(): ...") == []


def test_passes_modules_outside_layer_packages():
    assert check("src/pkg/a.py", classes(2) + functions(2)) == []
