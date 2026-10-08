from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class NameFromPackageViolation(Violation):
    """``source`` is the module that defines ``name``, if it is known."""

    package: str
    name: str
    source: str | None

    @property
    def message(self) -> str:
        source = self.source or "the module that defines it"
        return f"{self.package} is a package; import {self.name} from {source}"
