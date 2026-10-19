from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation_first_party_module_import import (
    ViolationFirstPartyModuleImport,
)
from lint_rules._stateful_computations.check_first_party_module_imports import (
    CheckFirstPartyModuleImports,
)


def test_first_party_module_import(subtests, fake_project):
    cases = [
        fake_project.case(
            "reports root package",
            fake_project.project().package("lib").check_module("lib.app", "import lib"),
            expected=[
                ViolationFirstPartyModuleImport(
                    "src/lib/app.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        fake_project.case(
            "reports import visited before its module is defined",
            fake_project.project().check_module("app", "import lib").package("lib"),
            expected=[
                ViolationFirstPartyModuleImport(
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
                ViolationFirstPartyModuleImport(
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
                fake_project.check(project, CheckFirstPartyModuleImports()) == expected
            )
