from lint_rules._stateless_computations.layer_package import layer_package


def test_layer_package(subtests):
    cases = [
        ("src/pkg/_entities/a.py", "_entities"),
        ("src/pkg/_stateful_effects/sub/a.py", "_stateful_effects"),
        ("src/pkg/a.py", None),
        ("src/pkg/entities/a.py", None),
    ]
    for path, expected in cases:
        with subtests.test(path):
            assert layer_package(path) == expected
