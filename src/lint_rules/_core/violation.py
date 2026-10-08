from abc import ABC, abstractmethod
from dataclasses import dataclass

from lint_rules._core.source.source_location import SourceLocation


@dataclass(frozen=True)
class Violation(ABC):
    """A rule violation; each rule has a subclass that holds what it found.

    Equality compares the type and the findings, never the text, so the
    wording lives only in each subclass's ``message``.
    """

    path: str
    location: SourceLocation | None = None

    @property
    @abstractmethod
    def message(self) -> str: ...

    def __str__(self) -> str:
        if self.location is None:
            return f"{self.path}: {self.message}"
        return f"{self.path}:{self.location.line}:{self.location.col}: {self.message}"
