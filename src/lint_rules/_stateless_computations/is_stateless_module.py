_STATELESS_LAYERS = frozenset(
    {
        "_stateless_computations",
        "_stateless_workflows",
        "_stateless_effects",
    }
)


def is_stateless_module(path: str) -> bool:
    """Whether the file lies in one of the ``_stateless_*`` packages."""
    return not _STATELESS_LAYERS.isdisjoint(path.split("/"))
