from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class UnimportedPublicNameViolation(Violation):
    name: str

    @property
    def message(self) -> str:
        return (
            f"public name {self.name} is not imported by any other module; "
            f"rename it to _{self.name} or delete it"
        )
