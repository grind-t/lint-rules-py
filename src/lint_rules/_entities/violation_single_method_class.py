from dataclasses import dataclass

from lint_rules._entities.violation import Violation


@dataclass(frozen=True, kw_only=True)
class ViolationSingleMethodClass(Violation):
    class_name: str
    method_name: str

    @property
    def message(self) -> str:
        return (
            f"class {self.class_name} has a single method {self.method_name}; "
            "use a function, a Callable alias or a Protocol with __call__"
        )
