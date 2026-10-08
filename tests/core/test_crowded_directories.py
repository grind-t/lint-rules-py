import pytest

from lint_rules._core.crowded_directories import crowded_directories


def _modules(directory: str, count: int) -> list[str]:
    return [f"{directory}/m{i}.py" for i in range(count)]


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        (_modules("src/lib", 3), []),
        (_modules("src/lib", 4), [("src/lib", 4)]),
        ([*_modules("src/lib", 3), "src/lib/__init__.py"], []),
        ([*_modules("src/lib", 3), "src/lib/notes.txt"], []),
        ([*_modules("src/lib", 2), *_modules("src/lib/sub", 2)], []),
        (
            [*_modules("src/lib", 2), *_modules("src/lib/sub", 4)],
            [("src/lib/sub", 4)],
        ),
        (
            [*_modules("src/b", 4), *_modules("src/a", 5)],
            [("src/a", 5), ("src/b", 4)],
        ),
        (["a.py", "b.py", "c.py", "d.py"], [(".", 4)]),
    ],
)
def test_crowded_directories(paths, expected):
    assert crowded_directories(paths, limit=3) == expected
