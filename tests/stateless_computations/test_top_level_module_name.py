from lint_rules._stateless_computations.top_level_module_name import (
    top_level_module_name,
)


def test_top_level_module_name(subtests):
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
            assert top_level_module_name(path, root) == expected
