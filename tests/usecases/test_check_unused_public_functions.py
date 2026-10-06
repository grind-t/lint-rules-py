import ast

from lint_rules._core.violation import Violation
from lint_rules._usecases.check_unused_public_functions import (
    CheckUnusedPublicFunctions,
)


def check(files: dict[str, str]) -> list[Violation]:
    checker = CheckUnusedPublicFunctions()
    for path, source in files.items():
        checker.visit(path, source, ast.parse(source))
    return checker.finish()


def test_reports_function_not_used_outside_module():
    assert check({"a.py": "x = 1\n\ndef helper(): ..."}) == [
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
