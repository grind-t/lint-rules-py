import ast
from dataclasses import replace

from lint_rules._core.candidate import Kind
from lint_rules._core.unused_public_names import (
    ModuleSummary,
    summarize_module,
    unused_public_names,
)
from lint_rules._core.violation import Violation

_MARKERS: dict[Kind, str] = {
    "function": "# allow-unused-public-functions",
    "variable": "# allow-unused-public-variables",
}


class CheckUnusedPublicNames:
    """Collects a summary of every file, then reports across all of them."""

    def __init__(self) -> None:
        self._summaries: list[ModuleSummary] = []

    def visit(self, path: str, source: str, tree: ast.Module) -> None:
        summary = summarize_module(path, tree)
        allowed = {kind for kind, marker in _MARKERS.items() if marker in source}
        if allowed:
            # The file's own names are exempt, but its imports still count.
            candidates = tuple(c for c in summary.candidates if c.kind not in allowed)
            summary = replace(summary, candidates=candidates)
        self._summaries.append(summary)

    def finish(self) -> list[Violation]:
        return [
            Violation(
                path,
                f"line {c.line}: {c.kind} {c.name} is not used outside the module; "
                f"rename it to _{c.name}",
            )
            for path, c in unused_public_names(self._summaries)
        ]
