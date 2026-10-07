from dataclasses import dataclass

from lint_rules._core.violation import Violation


@dataclass(frozen=True, kw_only=True)
class FirstPartyModuleImportViolation(Violation):
    module: str

    @property
    def message(self) -> str:
        return (
            f'"import {self.module}" binds a first-party module; '
            'use "from <module> import <name>" instead'
        )
