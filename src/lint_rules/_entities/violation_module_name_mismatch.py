from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationModuleNameMismatch(Violation):
    public_names: tuple[str, ...]

    @property
    def message(self) -> str:
        return (
            "module name matches none of its public names "
            f"({', '.join(self.public_names)}); "
            "rename the module after its main name"
        )
