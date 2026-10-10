from dataclasses import dataclass

from lint_rules._core.shared.violation import Violation


@dataclass(frozen=True, kw_only=True)
class PlainFirstPartyImportViolation(Violation):
    module: str

    @property
    def message(self) -> str:
        return (
            f'"import {self.module}" of a first-party module; '
            f'use "from {self.module} import <name>" instead'
        )
