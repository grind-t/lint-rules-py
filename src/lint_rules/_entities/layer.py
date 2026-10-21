from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Layer:
    """A layer package with what its modules may contain and do."""

    name: str
    public_class_limit: int
    public_function_limit: int
    is_pure: bool
