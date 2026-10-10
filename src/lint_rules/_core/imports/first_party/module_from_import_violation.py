from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class FirstPartyModuleFromImportViolation(Violation):
    module: str
    name: str

    @property
    def message(self) -> str:
        return (
            f'"from {self.module} import {self.name}" of a first-party module; '
            f'use "from {self.module}.{self.name} import <name>" instead'
        )
