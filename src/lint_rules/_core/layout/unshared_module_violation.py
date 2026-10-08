from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class UnsharedModuleViolation(Violation):
    features: tuple[str, ...]

    @property
    def message(self) -> str:
        if self.features:
            return (
                f"shared module used only by feature {self.features[0]}; "
                "move it into that feature"
            )
        return (
            "shared module used by no feature; move it to where it is used or delete it"
        )
