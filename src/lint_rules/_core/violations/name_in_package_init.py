from dataclasses import dataclass

from lint_rules._core.violation import Violation


@dataclass(frozen=True, kw_only=True)
class NameInPackageInitViolation(Violation):
    package: str
    name: str

    @property
    def message(self) -> str:
        return (
            f"{self.package} is a package; "
            f"move {self.name} from its __init__.py to a module"
        )
