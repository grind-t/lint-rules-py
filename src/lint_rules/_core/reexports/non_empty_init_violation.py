from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class NonEmptyInitViolation(Violation):
    @property
    def message(self) -> str:
        return (
            "__init__.py must be empty; "
            "re-exports are allowed only in a top-level package"
        )
