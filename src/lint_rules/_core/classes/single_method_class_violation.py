from dataclasses import dataclass

from lint_rules._core.violation import Violation


@dataclass(frozen=True, kw_only=True)
class SingleMethodClassViolation(Violation):
    cls: str
    method: str

    @property
    def message(self) -> str:
        return (
            f"class {self.cls} has a single method {self.method}; "
            "use a function, a Callable alias or a Protocol with __call__"
        )
