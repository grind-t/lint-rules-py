from dataclasses import dataclass

from lint_rules._core.violation import Violation


@dataclass(frozen=True, kw_only=True)
class StarImportViolation(Violation):
    module: str

    @property
    def message(self) -> str:
        return (
            f'"from {self.module} import *" hides which names are used; '
            "import them explicitly"
        )
