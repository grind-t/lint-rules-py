from dataclasses import dataclass


@dataclass(frozen=True)
class SourceFile:
    """A Python file as read."""

    root: str
    path: str
    source: str
