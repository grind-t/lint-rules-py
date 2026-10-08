from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ModuleImportedAsNameViolation(Violation):
    module: str

    @property
    def message(self) -> str:
        return (
            f"{self.module} is a module; "
            "import names from it instead of the module itself"
        )
