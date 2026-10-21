import ast

from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.ast_counted_public_classes import (
    ast_counted_public_classes,
)


def names(source: str) -> list[str]:
    return [name for name, _ in ast_counted_public_classes(ast.parse(source))]


def test_public_classes(subtests):
    cases = [
        ("class A: ...\nclass B: ...", ["A", "B"]),
        ("class A: ...\nclass _B: ...", ["A"]),
        ("class E(Exception): ...", []),
        ("class E(LibError): ...", []),
        ("class E(ValueError): ...\nclass F(E): ...", []),
        ("class K(Enum): ...", []),
        ("class K(enum.StrEnum): ...", []),
        ("class K(IntEnum): ...\nclass L(K): ...", []),
        ("class P(Protocol): ...", []),
        ("class P(typing.Protocol[T]): ...", []),
        ("class P(Protocol): ...\nclass Impl(P): ...", ["Impl"]),
        ("class G(ExceptionGroup): ...", []),
        ("class D(TypedDict): ...", ["D"]),
        ("class T(NamedTuple): ...", ["T"]),
        ("class A(Generic[T]): ...", ["A"]),
        ("class A:\n    class Inner: ...", ["A"]),
        ("def f() -> None:\n    class Local: ...", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert names(source) == expected


def test_locations():
    assert ast_counted_public_classes(ast.parse("x = 1\nclass A: ...")) == [
        ("A", SourceLocation(2, 1))
    ]
