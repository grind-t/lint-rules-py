import pytest

from lint_rules._core.source.module_name import module_name


@pytest.mark.parametrize(
    ("path", "root", "expected"),
    [
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
    ],
)
def test_module_name(path, root, expected):
    assert module_name(path, root) == expected
