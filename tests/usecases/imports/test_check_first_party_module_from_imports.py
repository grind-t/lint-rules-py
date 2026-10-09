from fake_project import Project, case, check

from lint_rules._core.imports.first_party_module_from_import_violation import (
    FirstPartyModuleFromImportViolation,
)
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._usecases.check_first_party_module_from_imports import (
    CheckFirstPartyModuleFromImports,
)


def lib() -> Project:
    return (
        Project()
        .package("lib")
        .package("lib._core")
        .module("lib._core.greeting", "class Greeting: ...")
    )


def test_first_party_module_from_import(subtests):
    cases = [
        case(
            "reports module",
            lib().check_module("lib.app", "from lib._core import greeting"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    module="lib._core",
                    name="greeting",
                )
            ],
        ),
        case(
            "reports package",
            lib().check_module("lib.app", "from lib import _core"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 17),
                    module="lib",
                    name="_core",
                )
            ],
        ),
        case(
            "reports module defined in file seen after the checked one",
            Project()
            .package("lib")
            .check_module("lib.a", "from lib import z")
            .module("lib.z"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/a.py", SourceLocation(1, 17), module="lib", name="z"
                )
            ],
        ),
        case(
            "passes name that is not a module",
            lib().check_module("lib.app", "from lib._core import Greeting"),
            expected=[],
        ),
        case(
            "passes third-party and standard library modules",
            lib().check_module(
                "lib.app",
                """
                from os import path
                from importlib import metadata
                """,
            ),
            expected=[],
        ),
        case(
            "passes module of root directory without __init__.py",
            Project()
            .module("scripts.build")
            .check_module("app", "from scripts import build"),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert check(project, CheckFirstPartyModuleFromImports()) == expected
