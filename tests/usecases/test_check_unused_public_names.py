import ast

import pytest

from lint_rules._core.violation import Violation
from lint_rules._usecases.check_unused_public_names import (
    CheckUnusedPublicNames,
)


def check(files: dict[str, str]) -> list[Violation]:
    checker = CheckUnusedPublicNames()
    for path, source in files.items():
        checker.visit(path, source, ast.parse(source))
    return checker.finish()


def test_reports_function_not_used_outside_module():
    assert check({"a.py": "_x = 1\n\ndef helper(): ..."}) == [
        Violation(
            "a.py",
            "line 3: function helper is not used outside the module; "
            "rename it to _helper",
        )
    ]


def test_passes_function_used_by_another_module():
    assert check({"a.py": "def helper(): ...", "b.py": "from a import helper"}) == []


def test_marker_disables_check():
    assert check({"a.py": "# allow-unused-public-functions\ndef helper(): ..."}) == []


def test_marked_module_still_uses_other_modules():
    files = {
        "a.py": "def helper(): ...",
        "b.py": "# allow-unused-public-functions\nfrom a import helper",
    }
    assert check(files) == []


def test_reports_variable_not_used_outside_module():
    assert check({"a.py": "LIMIT = 1"}) == [
        Violation(
            "a.py",
            "line 1: variable LIMIT is not used outside the module; "
            "rename it to _LIMIT",
        )
    ]


@pytest.mark.parametrize(
    ("marker", "kind", "name", "line"),
    [
        ("# allow-unused-public-variables", "function", "helper", 4),
        ("# allow-unused-public-functions", "variable", "LIMIT", 2),
    ],
)
def test_markers_are_per_kind(marker, kind, name, line):
    source = f"{marker}\nLIMIT = 1\n\ndef helper(): ..."
    assert check({"a.py": source}) == [
        Violation(
            "a.py",
            f"line {line}: {kind} {name} is not used outside the module; "
            f"rename it to _{name}",
        )
    ]
