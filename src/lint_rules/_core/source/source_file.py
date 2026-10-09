from dataclasses import dataclass


@dataclass(frozen=True)
class SourceFile:
    """A Python file as read."""

    path: str
    source: str
