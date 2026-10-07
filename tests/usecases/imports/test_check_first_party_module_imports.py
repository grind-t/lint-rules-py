import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violations.first_party_module_import import (
    FirstPartyModuleImportViolation,
)
from lint_rules._usecases.check_source_files import check_source_files


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports root package",
            Project().package("lib").check_module("lib.app", "import lib"),
            expected=[
                FirstPartyModuleImportViolation(
                    "src/lib/app.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        case(
            "reports module imported with alias",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .check_module("lib.app", "import lib._core.greeting as greeting"),
            expected=[
                FirstPartyModuleImportViolation(
                    "src/lib/app.py", SourceLocation(1, 8), module="lib._core.greeting"
                )
            ],
        ),
        case(
            "reports only first-party module of several",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .check_module("lib.app", "import os, lib._core.greeting"),
            expected=[
                FirstPartyModuleImportViolation(
                    "src/lib/app.py", SourceLocation(1, 12), module="lib._core.greeting"
                )
            ],
        ),
        # Only the first component matters; whether the module exists does not.
        case(
            "reports nonexistent first-party module",
            Project().package("lib").check_module("lib.app", "import lib._nope"),
            expected=[
                FirstPartyModuleImportViolation(
                    "src/lib/app.py", SourceLocation(1, 8), module="lib._nope"
                )
            ],
        ),
        case(
            "reports top-level module",
            Project().module("single").check_module("app", "import single"),
            expected=[
                FirstPartyModuleImportViolation(
                    "src/app.py", SourceLocation(1, 8), module="single"
                )
            ],
        ),
        case(
            "reports import in function",
            Project()
            .package("lib")
            .check_module(
                "lib.app",
                """
                def f():
                    import lib._core.greeting
                """,
            ),
            expected=[
                FirstPartyModuleImportViolation(
                    "src/lib/app.py", SourceLocation(2, 12), module="lib._core.greeting"
                )
            ],
        ),
        # Not importable, but still checked.
        case(
            "checks file without module name",
            Project().package("lib").check_file("my-dir/x.py", "import lib"),
            expected=[
                FirstPartyModuleImportViolation(
                    "src/my-dir/x.py", SourceLocation(1, 8), module="lib"
                )
            ],
        ),
        case(
            "passes third-party module",
            Project().check_module(
                "app",
                """
                import os
                import os.path
                """,
            ),
            expected=[],
        ),
        case(
            "passes name that only starts with first-party name",
            Project()
            .package("lib")
            .check_module(
                "lib.app",
                """
                import library
                import lib_extra
                """,
            ),
            expected=[],
        ),
        case(
            "passes root directory without __init__.py",
            Project().module("scripts.build").check_module("app", "import scripts"),
            expected=[],
        ),
    ],
)
def test_import_of_first_party_module(project, expected):
    assert check(project) == expected


def test_current_directory_as_root():
    files = {"lib/__init__.py": "", "lib/x.py": "import lib"}
    assert check_source_files(lambda _roots: files.items(), ["."]) == [
        FirstPartyModuleImportViolation("lib/x.py", SourceLocation(1, 8), module="lib")
    ]
