from lint_rules._core.imports.plain_first_party_import_violation import (
    PlainFirstPartyImportViolation,
)
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._usecases.imports.check_plain_first_party_imports import (
    CheckPlainFirstPartyImports,
)


def test_plain_first_party_import(subtests, fake_project):
    cases = [
        fake_project.case(
            "reports root package",
            fake_project.project().package("lib").check_module("lib.app", "import lib"),
            expected=[
                PlainFirstPartyImportViolation(
                    "src/lib/app.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        fake_project.case(
            "reports import visited before its module is defined",
            fake_project.project().check_module("app", "import lib").package("lib"),
            expected=[
                PlainFirstPartyImportViolation(
                    "src/app.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        # Not importable, but still checked.
        fake_project.case(
            "checks file without module name",
            fake_project.project()
            .package("lib")
            .check_file("my-dir/x.py", "import lib"),
            expected=[
                PlainFirstPartyImportViolation(
                    "src/my-dir/x.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        fake_project.case(
            "passes third-party module",
            fake_project.project().check_module("app", "import os"),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert (
                fake_project.check(project, CheckPlainFirstPartyImports()) == expected
            )
