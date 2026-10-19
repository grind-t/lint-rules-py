_STATEFUL_LAYERS = frozenset(
    {
        "_stateful_computations",
        "_stateful_workflows",
        "_stateful_effects",
    }
)


def is_stateful_module(path: str) -> bool:
    """Whether the file lies in one of the ``_stateful_*`` packages."""
    return not _STATEFUL_LAYERS.isdisjoint(path.split("/"))
