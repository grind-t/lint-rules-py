from lint_rules._core.imports.first_party import is_first_party


def test_is_first_party(subtests):
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
            assert is_first_party(module, top_level_modules) == expected
