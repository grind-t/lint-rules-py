from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationFirstPartyModuleImportFrom(Violation):
    module: str
    submodule: str

    @property
    def message(self) -> str:
        return (
            f'"from {self.module} import {self.submodule}" of a first-party module; '
            f'use "from {self.module}.{self.submodule} import <name>" instead'
        )
