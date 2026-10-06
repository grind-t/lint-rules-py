import ast
from dataclasses import replace

from lint_rules._core.unused_public_functions import (
    ModuleSummary,
    summarize_module,
    unused_public_functions,
)
from lint_rules._core.violation import Violation

MARKER = "# allow-unused-public-functions"


class CheckUnusedPublicFunctions:
    """Collects a summary of every file, then reports across all of them."""

    def __init__(self) -> None:
        self._summaries: list[ModuleSummary] = []

    def visit(self, path: str, source: str, tree: ast.Module) -> None:
        summary = summarize_module(path, tree)
        if MARKER in source:
            # The file's own functions are exempt, but its imports still count.
            summary = replace(summary, candidates=())
        self._summaries.append(summary)

    def finish(self) -> list[Violation]:
        return [
            Violation(
                path,
                f"line {line}: function {name} is not used outside the module; "
                f"rename it to _{name}",
            )
            for path, name, line in unused_public_functions(self._summaries)
        ]
