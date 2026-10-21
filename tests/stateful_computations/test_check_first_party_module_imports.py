from lint_rules._entities.source_location import SourceLocation
from lint_rules._entities.violation_first_party_module_import import (
    ViolationFirstPartyModuleImport,
)
from lint_rules._entities.violation_first_party_module_import_from import (
    ViolationFirstPartyModuleImportFrom,
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


def lib(fake_project):
    return (
        fake_project.project()
        .package("lib")
        .package("lib._core")
        .module("lib._core.greeting", "class Greeting: ...")
    )


def test_first_party_module_import_from(subtests, fake_project):
    cases = [
        fake_project.case(
            "reports module",
            lib(fake_project).check_module("lib.app", "from lib._core import greeting"),
            expected=[
                ViolationFirstPartyModuleImportFrom(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    module="lib._core",
                    submodule="greeting",
                )
            ],
        ),
        fake_project.case(
            "reports package",
            lib(fake_project).check_module("lib.app", "from lib import _core"),
            expected=[
                ViolationFirstPartyModuleImportFrom(
                    "src/lib/app.py",
                    SourceLocation(1, 17),
                    module="lib",
                    submodule="_core",
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
                ViolationFirstPartyModuleImportFrom(
                    "src/lib/a.py", SourceLocation(1, 17), module="lib", submodule="z"
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
                fake_project.check(project, CheckFirstPartyModuleImports()) == expected
            )
