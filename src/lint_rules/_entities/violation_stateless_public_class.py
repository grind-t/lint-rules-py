from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationStatelessPublicClass(Violation):
    name: str

    @property
    def message(self) -> str:
        return (
            f"public class {self.name} in a stateless package; "
            "use functions, or move it to _entities"
        )
