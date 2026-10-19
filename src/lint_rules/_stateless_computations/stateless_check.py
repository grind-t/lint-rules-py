from collections.abc import Callable

from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation

type StatelessCheck = Callable[[ParsedFile], list[Violation]]
