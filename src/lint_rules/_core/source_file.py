from dataclasses import dataclass


@dataclass(frozen=True)
class SourceFile:
    """A Python file as read, with the root it was found under."""

    root: str
    path: str
    source: str
