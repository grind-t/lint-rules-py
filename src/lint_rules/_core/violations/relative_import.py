from dataclasses import dataclass

from lint_rules._core.violation import Violation


@dataclass(frozen=True, kw_only=True)
class RelativeImportViolation(Violation):
    """``absolute`` is the module the import resolves to, if it resolves."""

    absolute: str | None

    @property
    def message(self) -> str:
        if self.absolute is None:
            return "relative import; use an absolute import instead"
        return f'relative import; use "from {self.absolute} import ..." instead'
