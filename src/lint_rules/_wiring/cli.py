import sys

from lint_rules._adapters.fs_source_files import read_fs_source_files
from lint_rules._usecases.check_source_files import check_source_files


def main(argv: list[str] | None = None) -> int:
    roots = (sys.argv[1:] if argv is None else argv) or ["src"]
    violations = check_source_files(read_fs_source_files, roots)
    for violation in violations:
        sys.stderr.write(f"{violation}\n")
    return int(bool(violations))
