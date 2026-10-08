from dataclasses import dataclass

from lint_rules._core.violation import Violation


@dataclass(frozen=True, kw_only=True)
class CrowdedDirectoryViolation(Violation):
    modules: int
    limit: int

    @property
    def message(self) -> str:
        return (
            f"{self.modules} modules in one directory, more than {self.limit}; "
            "run a subagent that reads them and groups related modules into "
            "subpackages by meaning, not into catch-alls like utils or helpers"
        )
