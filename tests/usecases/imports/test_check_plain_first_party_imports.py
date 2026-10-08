import pytest
from fake_project import Project, case, check, check_files

from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_file import SourceFile
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._core.violations.plain_first_party_import import (
    PlainFirstPartyImportViolation,
)
from lint_rules._usecases.check_plain_first_party_imports import (
    CheckPlainFirstPartyImports,
)


@pytest.mark.parametrize(
    ("project", "expected"),
    [
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
            "reports module imported with alias",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .check_module("lib.app", "import lib._core.greeting as greeting"),
            expected=[
                PlainFirstPartyImportViolation(
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
                PlainFirstPartyImportViolation(
                    "src/lib/app.py", SourceLocation(1, 12), module="lib._core.greeting"
                )
            ],
        ),
        # Only the first component matters; whether the module exists does not.
        case(
            "reports nonexistent first-party module",
            Project().package("lib").check_module("lib.app", "import lib._nope"),
            expected=[
                PlainFirstPartyImportViolation(
                    "src/lib/app.py", SourceLocation(1, 8), module="lib._nope"
                )
            ],
        ),
        case(
            "reports top-level module",
            Project().module("single").check_module("app", "import single"),
            expected=[
                PlainFirstPartyImportViolation(
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
                PlainFirstPartyImportViolation(
                    "src/lib/app.py", SourceLocation(2, 12), module="lib._core.greeting"
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
def test_plain_first_party_import(project, expected):
    assert check(project, CheckPlainFirstPartyImports()) == expected


def test_current_directory_as_root():
    files = [
        SourceFile(".", "lib/__init__.py", ""),
        SourceFile(".", "lib/x.py", "import lib"),
    ]
    assert check_files(
        [ParsedFile(f) for f in files], CheckPlainFirstPartyImports()
    ) == [
        PlainFirstPartyImportViolation("lib/x.py", SourceLocation(1, 8), module="lib")
    ]


def test_top_level_modules_of_every_root():
    files = [
        SourceFile("tests", "tests/conftest.py", ""),
        SourceFile("src", "src/lib/x.py", "import conftest"),
    ]
    assert check_files(
        [ParsedFile(f) for f in files], CheckPlainFirstPartyImports()
    ) == [
        PlainFirstPartyImportViolation(
            "src/lib/x.py", SourceLocation(1, 8), module="conftest"
        )
    ]
