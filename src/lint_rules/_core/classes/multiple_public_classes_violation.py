from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class MultiplePublicClassesViolation(Violation):
    classes: tuple[str, ...]

    @property
    def message(self) -> str:
        return (
            f"{len(self.classes)} public classes ({', '.join(self.classes)}); "
            "split them into separate modules"
        )
