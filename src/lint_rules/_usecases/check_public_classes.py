from lint_rules._core.parsed_file import ParsedFile
from lint_rules._core.public_classes import public_classes
from lint_rules._core.violation import Violation

_MARKER = "# allow-multiple-public-classes"


def check_public_classes(file: ParsedFile) -> list[Violation]:
    if _MARKER in file.source:
        return []
    classes = public_classes(file.tree)
    if len(classes) <= 1:
        return []
    message = (
        f"{len(classes)} public classes ({', '.join(classes)}); "
        "split them into separate modules"
    )
    return [Violation(file.path, message)]
