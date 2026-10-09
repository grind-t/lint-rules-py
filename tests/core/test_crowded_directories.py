from lint_rules._core.layout.crowded_directories import crowded_directories


def _modules(directory: str, count: int) -> list[str]:
    return [f"{directory}/m{i}.py" for i in range(count)]


def test_crowded_directories(subtests):
    cases = {
        "at limit": (_modules("src/lib", 3), []),
        "over limit": (_modules("src/lib", 4), [("src/lib", 4)]),
        "init ignored": ([*_modules("src/lib", 3), "src/lib/__init__.py"], []),
        "non-python ignored": ([*_modules("src/lib", 3), "src/lib/notes.txt"], []),
        "subdirectory counted separately": (
            [*_modules("src/lib", 2), *_modules("src/lib/sub", 2)],
            [],
        ),
        "only crowded subdirectory reported": (
            [*_modules("src/lib", 2), *_modules("src/lib/sub", 4)],
            [("src/lib/sub", 4)],
        ),
        "sorted by path": (
            [*_modules("src/b", 4), *_modules("src/a", 5)],
            [("src/a", 5), ("src/b", 4)],
        ),
        "root directory": (["a.py", "b.py", "c.py", "d.py"], [(".", 4)]),
    }
    for name, (paths, expected) in cases.items():
        with subtests.test(name):
            assert crowded_directories(paths, limit=3) == expected
