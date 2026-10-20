from lint_rules._stateless_computations.layer_of import layer_of


def test_layer_of(subtests):
    cases = [
        ("src/pkg/_entities/a.py", "_entities"),
        ("src/pkg/_stateful_effects/sub/a.py", "_stateful_effects"),
        ("src/pkg/a.py", None),
        ("src/pkg/entities/a.py", None),
    ]
    for path, expected in cases:
        with subtests.test(path):
            layer = layer_of(path)
            assert (None if layer is None else layer.name) == expected
