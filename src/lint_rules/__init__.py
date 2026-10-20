import argparse

from lint_rules._entities.violation import Violation
from lint_rules._stateless_effects.read_fs_source_files import read_fs_source_files
from lint_rules._stateless_effects.report_to_stderr import report_to_stderr
from lint_rules._stateless_workflows.lint import lint


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default="src")
    args = parser.parse_args(argv)
    return int(bool(lint(read_fs_source_files(args.root), report_to_stderr)))


__all__ = ["Violation", "main"]
