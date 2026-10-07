from dataclasses import dataclass

from lint_rules._core.source_location import SourceLocation


@dataclass(frozen=True)
class Violation:
    path: str
    message: str
    location: SourceLocation | None = None

    def __str__(self) -> str:
        if self.location is None:
            return f"{self.path}: {self.message}"
        return f"{self.path}:{self.location.line}:{self.location.col}: {self.message}"
