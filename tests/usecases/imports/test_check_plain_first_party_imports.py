from fake_project import Project, case, check

from lint_rules._core.imports.plain_first_party_import_violation import (
    PlainFirstPartyImportViolation,
)
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._usecases.check_plain_first_party_imports import (
    CheckPlainFirstPartyImports,
)


def test_plain_first_party_import(subtests):
    cases = [
        case(
            "reports root package",
            Project().package("lib").check_module("lib.app", "import lib"),
            expected=[
                PlainFirstPartyImportViolation(
                    "src/lib/app.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        case(
            "reports import visited before its module is defined",
            Project().check_module("app", "import lib").package("lib"),
            expected=[
                PlainFirstPartyImportViolation(
                    "src/app.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        # Not importable, but still checked.
        case(
            "checks file without module name",
            Project().package("lib").check_file("my-dir/x.py", "import lib"),
            expected=[
                PlainFirstPartyImportViolation(
                    "src/my-dir/x.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        case(
            "passes third-party module",
            Project().check_module("app", "import os"),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert check(project, CheckPlainFirstPartyImports("src")) == expected
