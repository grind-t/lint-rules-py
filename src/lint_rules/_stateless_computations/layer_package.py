_LAYER_PACKAGES = frozenset(
    {
        "_entities",
        "_stateless_computations",
        "_stateless_workflows",
        "_stateless_effects",
        "_stateful_computations",
        "_stateful_workflows",
        "_stateful_effects",
    }
)


def layer_package(path: str) -> str | None:
    """Name of the layer package the file lies in, e.g. ``_entities``."""
    return next((part for part in path.split("/") if part in _LAYER_PACKAGES), None)
