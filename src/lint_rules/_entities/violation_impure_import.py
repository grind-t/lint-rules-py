from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationImpureImport(Violation):
    import_text: str

    @property
    def message(self) -> str:
        return f'"{self.import_text}" can do I/O; import only its pure names'
