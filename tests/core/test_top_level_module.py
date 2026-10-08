import pytest

from lint_rules._core.top_level_module import top_level_module


@pytest.mark.parametrize(
    ("path", "root", "expected"),
    [
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
        ("a.py", "src", None),
    ],
)
def test_top_level_module(path, root, expected):
    assert top_level_module(path, root) == expected
