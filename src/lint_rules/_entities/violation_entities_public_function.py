from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationEntitiesPublicFunction(Violation):
    name: str

    @property
    def message(self) -> str:
        return (
            f"public function {self.name} in _entities; "
            "make it a method or move it to a computations package"
        )
