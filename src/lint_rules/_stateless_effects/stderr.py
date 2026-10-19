import sys

from lint_rules._entities.violation import Violation


def report_to_stderr(violation: Violation) -> None:
    """Write the violation as one line to stderr."""
    sys.stderr.write(f"{violation}\n")
