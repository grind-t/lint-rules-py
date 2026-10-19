from lint_rules._stateless_computations.is_first_party_module import (
    is_first_party_module,
)


def test_is_first_party_module(subtests):
    top_level_modules = {"lib"}
    cases = [
        ("lib", True),
        ("lib.sub.mod", True),
        ("other", False),
        ("other.lib", False),
        ("libx", False),
    ]
    for module, expected in cases:
        with subtests.test(module):
            assert is_first_party_module(module, top_level_modules) == expected
