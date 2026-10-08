from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ModuleGetattrViolation(Violation):
    @property
    def message(self) -> str:
        return "module-level __getattr__ makes names dynamic; define them explicitly"
