from lint_rules._core.imports.top_level_module import top_level_module


def test_top_level_module(subtests):
    cases = [
        ("src/lib/__init__.py", "src", "lib"),
        ("src/single.py", "src", "single"),
        ("src/single.py", "src/", "single"),
        ("lib/__init__.py", ".", "lib"),
        ("./single.py", ".", "single"),
        ("src/__init__.py", "src", None),
        ("src/lib/app.py", "src", None),
        ("src/lib/sub/__init__.py", "src", None),
        ("src/notes.txt", "src", None),
        ("srcx/single.py", "src", None),
    ]
    for path, root, expected in cases:
        with subtests.test(f"{path} (root {root})"):
            assert top_level_module(path, root) == expected
