from lint_rules._core.imports.first_party_module_from_import_violation import (
    FirstPartyModuleFromImportViolation,
)
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._usecases.imports.check_first_party_module_from_imports import (
    CheckFirstPartyModuleFromImports,
)


def lib(fake_project):
    return (
        fake_project.project()
        .package("lib")
        .package("lib._core")
        .module("lib._core.greeting", "class Greeting: ...")
    )


def test_first_party_module_from_import(subtests, fake_project):
    cases = [
        fake_project.case(
            "reports module",
            lib(fake_project).check_module("lib.app", "from lib._core import greeting"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    module="lib._core",
                    name="greeting",
                )
            ],
        ),
        fake_project.case(
            "reports package",
            lib(fake_project).check_module("lib.app", "from lib import _core"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 17),
                    module="lib",
                    name="_core",
                )
            ],
        ),
        fake_project.case(
            "reports module defined in file seen after the checked one",
            fake_project.project()
            .package("lib")
            .check_module("lib.a", "from lib import z")
            .module("lib.z"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/a.py", SourceLocation(1, 17), module="lib", name="z"
                )
            ],
        ),
        fake_project.case(
            "passes name that is not a module",
            lib(fake_project).check_module("lib.app", "from lib._core import Greeting"),
            expected=[],
        ),
        fake_project.case(
            "passes third-party and standard library modules",
            lib(fake_project).check_module(
                "lib.app",
                """
                from os import path
                from importlib import metadata
                """,
            ),
            expected=[],
        ),
        fake_project.case(
            "passes module of root directory without __init__.py",
            fake_project.project()
            .module("scripts.build")
            .check_module("app", "from scripts import build"),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert (
                fake_project.check(project, CheckFirstPartyModuleFromImports())
                == expected
            )
