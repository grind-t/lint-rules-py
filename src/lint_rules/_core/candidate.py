from dataclasses import dataclass
from typing import Literal

type Kind = Literal["function", "variable"]


@dataclass(frozen=True)
class Candidate:
    """A public top-level name that must be used by another module."""

    kind: Kind
    name: str
    line: int
