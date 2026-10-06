import sys

from lint_rules._adapters.fs_source_files import read_fs_source_files
from lint_rules._usecases.check_public_classes import check_public_classes
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)


def main(argv: list[str] | None = None) -> int:
    roots = (sys.argv[1:] if argv is None else argv) or ["src"]
    violations = [
        *check_public_classes(read_fs_source_files, roots),
        *check_single_method_classes(read_fs_source_files, roots),
    ]
    for violation in violations:
        sys.stderr.write(f"{violation}\n")
    return int(bool(violations))
