from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationModuleNameMismatch(Violation):
    names: tuple[str, ...]

    @property
    def message(self) -> str:
        return (
            f"module name matches none of its public names ({', '.join(self.names)}); "
            "rename the module after its main name"
        )
