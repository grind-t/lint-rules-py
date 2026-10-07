from dataclasses import dataclass

from lint_rules._core.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ReexportedModuleViolation(Violation):
    """``name`` is bound in ``module`` by importing ``imported``."""

    name: str
    module: str
    imported: str

    @property
    def message(self) -> str:
        return (
            f"{self.name} is not defined in {self.module}, "
            f"only imported there as module {self.imported}"
        )
