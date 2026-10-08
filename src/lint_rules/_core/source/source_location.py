from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class SourceLocation:
    """1-based line and column."""

    line: int
    col: int
