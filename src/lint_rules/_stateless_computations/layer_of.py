from lint_rules._entities.layer import Layer

_LAYERS = {
    layer.name: layer
    for layer in (
        # name, max public classes, max public functions, does I/O
        Layer("_entities", 1, 0, False),
        Layer("_stateless_computations", 0, 1, False),
        Layer("_stateless_workflows", 0, 1, False),
        Layer("_stateless_effects", 0, 1, True),
        Layer("_stateful_computations", 1, 0, False),
        Layer("_stateful_workflows", 1, 0, False),
        Layer("_stateful_effects", 1, 0, True),
    )
}


def layer_of(path: str) -> Layer | None:
    """The layer package the file lies in, e.g. ``_entities``."""
    return next((_LAYERS[part] for part in path.split("/") if part in _LAYERS), None)
