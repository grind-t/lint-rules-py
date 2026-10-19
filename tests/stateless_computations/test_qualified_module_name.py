from lint_rules._stateless_computations.qualified_module_name import (
    qualified_module_name,
)


def test_qualified_module_name(subtests):
    cases = [
        ("src/lib/app.py", "src", "lib.app"),
        ("src/lib/app.py", "src/", "lib.app"),
        ("src/lib/__init__.py", "src", "lib"),
        ("src/lib/sub/__init__.py", "src", "lib.sub"),
        ("src/single.py", "src", "single"),
        ("lib/app.py", ".", "lib.app"),
        ("./lib/app.py", ".", "lib.app"),
        ("src/__init__.py", "src", None),
        ("src/notes.txt", "src", None),
        ("srcx/app.py", "src", None),
    ]
    for path, root, expected in cases:
        with subtests.test(f"{path} (root {root})"):
            assert qualified_module_name(path, root) == expected
