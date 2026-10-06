from collections.abc import Iterable

from lint_rules._core.public_classes import public_classes
from lint_rules._core.violation import Violation
from lint_rules._ports.source_files import SourceFiles

MARKER = "# allow-multiple-public-classes"


def check_public_classes(files: SourceFiles, roots: Iterable[str]) -> list[Violation]:
    violations = []
    for path, source in files.read_all(roots):
        if MARKER in source:
            continue
        classes = public_classes(source)
        if len(classes) > 1:
            message = (
                f"{len(classes)} public classes ({', '.join(classes)}); "
                "split them into separate modules"
            )
            violations.append(Violation(path, message))
    return violations
