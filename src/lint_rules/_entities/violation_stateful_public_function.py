from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationStatefulPublicFunction(Violation):
    name: str

    @property
    def message(self) -> str:
        return (
            f"public function {self.name} in a stateful package; "
            "make it a method or move it to a stateless package"
        )
