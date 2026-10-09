from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class CrowdedDirectoryViolation(Violation):
    modules: int
    limit: int

    @property
    def message(self) -> str:
        return (
            f"{self.modules} modules in one directory, more than {self.limit}; "
            "run a subagent that reads them and groups them into subpackages; "
            "put code used by more than one of those features into shared/"
        )
