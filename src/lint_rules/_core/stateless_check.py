from collections.abc import Callable

from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile

type StatelessCheck = Callable[[ParsedFile], list[Violation]]
