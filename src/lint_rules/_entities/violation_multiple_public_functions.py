from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationMultiplePublicFunctions(Violation):
    functions: tuple[str, ...]

    @property
    def message(self) -> str:
        return (
            f"{len(self.functions)} public functions ({', '.join(self.functions)}); "
            "split them into separate modules"
        )
