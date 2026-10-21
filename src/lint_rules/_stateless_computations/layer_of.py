from lint_rules._entities.layer import Layer

_LAYERS = {
    layer.name: layer
    for layer in (
        Layer(
            name="_entities",
            public_class_limit=1,
            public_function_limit=0,
            is_pure=True,
        ),
        Layer(
            name="_stateless_computations",
            public_class_limit=0,
            public_function_limit=1,
            is_pure=True,
        ),
        Layer(
            name="_stateless_workflows",
            public_class_limit=0,
            public_function_limit=1,
            is_pure=True,
        ),
        Layer(
            name="_stateless_effects",
            public_class_limit=0,
            public_function_limit=1,
            is_pure=False,
        ),
        Layer(
            name="_stateful_computations",
            public_class_limit=1,
            public_function_limit=0,
            is_pure=True,
        ),
        Layer(
            name="_stateful_workflows",
            public_class_limit=1,
            public_function_limit=0,
            is_pure=True,
        ),
        Layer(
            name="_stateful_effects",
            public_class_limit=1,
            public_function_limit=0,
            is_pure=False,
        ),
    )
}


def layer_of(path: str) -> Layer | None:
    """The layer package the file lies in, e.g. ``_entities``."""
    return next((_LAYERS[part] for part in path.split("/") if part in _LAYERS), None)
