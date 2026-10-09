from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ImpureImportViolation(Violation):
    statement: str

    @property
    def message(self) -> str:
        return f'"{self.statement}" can do I/O; import only its pure names'
