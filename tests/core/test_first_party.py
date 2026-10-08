import pytest

from lint_rules._core.first_party import is_first_party


@pytest.mark.parametrize(
    ("module", "expected"),
    [
        ("lib", True),
        ("lib.sub.mod", True),
        ("other", False),
        ("other.lib", False),
        ("libx", False),
    ],
)
def test_is_first_party(module, expected):
    assert is_first_party(module, {"lib"}) == expected
