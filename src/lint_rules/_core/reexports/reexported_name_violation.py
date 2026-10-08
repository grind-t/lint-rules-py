from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ReexportedNameViolation(Violation):
    """``name`` is imported into ``module`` as ``source_name`` from ``source``.

    ``source`` is None when it is unknown, as for a relative import.
    """

    name: str
    module: str
    source: str | None
    source_name: str

    @property
    def message(self) -> str:
        fix = (
            "import it from the module that defines it"
            if self.source is None
            else f"import {self.source_name} from {self.source}"
        )
        return (
            f"{self.name} is not defined in {self.module}, only imported there; {fix}"
        )
