from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationTooManyPublicNames(Violation):
    package: str
    limit: int
    kind: str
    names: tuple[str, ...]

    @property
    def message(self) -> str:
        return (
            f"{len(self.names)} public {self.kind} ({', '.join(self.names)}) "
            f"in {self.package}, at most {self.limit} allowed"
        )
