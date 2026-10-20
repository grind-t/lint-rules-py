from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    """A layer package with what its modules may contain and do."""

    name: str
    max_public_classes: int
    max_public_functions: int
    does_io: bool
