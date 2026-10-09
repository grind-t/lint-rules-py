from lint_rules._core.layout.unshared_module_violation import UnsharedModuleViolation


def test_message_names_the_feature():
    violation = UnsharedModuleViolation("src/lib/shared/base.py", features=("a",))
    assert "feature a" in violation.message
