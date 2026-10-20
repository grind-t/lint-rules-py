from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationTooManyPublicFunctions(Violation):
    package: str
    limit: int
    functions: tuple[str, ...]

    @property
    def message(self) -> str:
        return (
            f"{len(self.functions)} public functions ({', '.join(self.functions)}) "
            f"in {self.package}, at most {self.limit} allowed"
        )
