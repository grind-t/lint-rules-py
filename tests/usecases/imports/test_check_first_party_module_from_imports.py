import pytest
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


@pytest.mark.parametrize(
    ("project", "expected"),
    [
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
            "reports module imported with alias",
            lib().check_module("lib.app", "from lib._core import greeting as g"),
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
            "reports only module of several names",
            lib().check_module("lib.app", "from lib._core import Other, greeting"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 30),
                    module="lib._core",
                    name="greeting",
                )
            ],
        ),
        case(
            "reports import in function",
            lib().check_module(
                "lib.app",
                """
                def f():
                    from lib._core import greeting
                """,
            ),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/app.py",
                    SourceLocation(2, 27),
                    module="lib._core",
                    name="greeting",
                )
            ],
        ),
        case(
            "reports module imported from top-level module",
            Project()
            .package("lib")
            .module("lib.a")
            .check_module("app", "from lib import a"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/app.py", SourceLocation(1, 17), module="lib", name="a"
                )
            ],
        ),
        case(
            "reports module in package init",
            lib().check_package("lib._core", "from lib._core import greeting"),
            expected=[
                FirstPartyModuleFromImportViolation(
                    "src/lib/_core/__init__.py",
                    SourceLocation(1, 23),
                    module="lib._core",
                    name="greeting",
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
            "passes name from module",
            lib().check_module("lib.app", "from lib._core.greeting import Greeting"),
            expected=[],
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
            "passes relative import",
            lib().check_module("lib.app", "from . import _core"),
            expected=[],
        ),
        case(
            "passes star import",
            lib().check_module("lib.app", "from lib._core import *"),
            expected=[],
        ),
        case(
            "passes plain import",
            lib().check_module("lib.app", "import lib._core.greeting"),
            expected=[],
        ),
        case(
            "passes module of root directory without __init__.py",
            Project()
            .module("scripts.build")
            .check_module("app", "from scripts import build"),
            expected=[],
        ),
    ],
)
def test_first_party_module_from_import(project, expected):
    assert check(project, CheckFirstPartyModuleFromImports()) == expected
