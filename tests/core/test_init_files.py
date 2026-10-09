from lint_rules._core.reexports.init_files import is_top_level_init


def test_is_top_level_init(subtests):
    cases = [
        ("package directly under root", "src/lib/__init__.py", "src", True),
        ("another package under root", "src/other/__init__.py", "src", True),
        ("root itself", "src/__init__.py", "src", True),
        ("package under dot root", "lib/__init__.py", ".", True),
        ("nested package", "src/lib/core/__init__.py", "src", False),
        ("nested package under dot root", "lib/core/__init__.py", ".", False),
        ("module", "src/lib/app.py", "src", False),
        ("outside root", "tests/lib/__init__.py", "src", False),
    ]
    for description, path, root, expected in cases:
        with subtests.test(description):
            assert is_top_level_init(path, root) is expected
