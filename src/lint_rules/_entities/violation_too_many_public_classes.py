from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationTooManyPublicClasses(Violation):
    package: str
    limit: int
    classes: tuple[str, ...]

    @property
    def message(self) -> str:
        return (
            f"{len(self.classes)} public classes ({', '.join(self.classes)}) "
            f"in {self.package}, at most {self.limit} allowed; "
            "split them into modules or move them to another package"
        )
