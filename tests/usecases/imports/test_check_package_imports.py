import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violations.module_imported_as_name import (
    ModuleImportedAsNameViolation,
)
from lint_rules._core.violations.name_from_package import NameFromPackageViolation
from lint_rules._core.violations.name_in_package_init import NameInPackageInitViolation


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "passes name from module",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting", "def format_greeting(): ...")
            .check_module("lib.app", "from lib._core.greeting import format_greeting"),
            expected=[],
        ),
        case(
            "reports submodule imported as name",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .check_module("lib.app", "from lib._core import greeting"),
            expected=[
                ModuleImportedAsNameViolation(
                    "src/lib/app.py", SourceLocation(1, 23), module="lib._core.greeting"
                )
            ],
        ),
        case(
            "reports subpackage imported as name",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib import _core"),
            expected=[
                ModuleImportedAsNameViolation(
                    "src/lib/app.py", SourceLocation(1, 17), module="lib._core"
                )
            ],
        ),
        case(
            "reports name imported into package __init__.py",
            Project()
            .package("lib")
            .package("lib._core", "from lib._core.greeting import format_greeting")
            .module("lib._core.greeting", "def format_greeting(): ...")
            .check_module("lib.app", "from lib._core import format_greeting"),
            expected=[
                NameFromPackageViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    package="lib._core",
                    name="format_greeting",
                    source="lib._core.greeting",
                )
            ],
        ),
        case(
            "reports each name at its own position",
            Project()
            .package("lib")
            .package("lib._core", "from lib._core.greeting import format_greeting")
            .module("lib._core.greeting", "def format_greeting(): ...")
            .check_module(
                "lib.app",
                """
                from lib._core import (
                    format_greeting,
                    greeting,
                )
                """,
            ),
            expected=[
                NameFromPackageViolation(
                    "src/lib/app.py",
                    SourceLocation(2, 5),
                    package="lib._core",
                    name="format_greeting",
                    source="lib._core.greeting",
                ),
                ModuleImportedAsNameViolation(
                    "src/lib/app.py", SourceLocation(3, 5), module="lib._core.greeting"
                ),
            ],
        ),
        # A definition in __init__.py does not make importing from a package fine.
        case(
            "reports name defined in package __init__.py",
            Project()
            .package("lib")
            .package("lib._core", 'DEFAULT_NAME = "world"')
            .check_module("lib.app", "from lib._core import DEFAULT_NAME"),
            expected=[
                NameInPackageInitViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    package="lib._core",
                    name="DEFAULT_NAME",
                )
            ],
        ),
        # At runtime the result depends on whether the submodule is already imported.
        case(
            "reports submodule shadowing name in package __init__.py",
            Project()
            .package("lib")
            .package("lib._core", 'greeting = "hi"')
            .module("lib._core.greeting")
            .check_module("lib.app", "from lib._core import greeting"),
            expected=[
                ModuleImportedAsNameViolation(
                    "src/lib/app.py", SourceLocation(1, 23), module="lib._core.greeting"
                )
            ],
        ),
        # lib._extra has no __init__.py.
        case(
            "reports submodule of namespace package",
            Project()
            .package("lib")
            .module("lib._extra.plugin")
            .check_module("lib.app", "from lib._extra import plugin"),
            expected=[
                ModuleImportedAsNameViolation(
                    "src/lib/app.py", SourceLocation(1, 24), module="lib._extra.plugin"
                )
            ],
        ),
        case(
            "reports name from namespace package",
            Project()
            .package("lib")
            .module("lib._extra.plugin", "def run(): ...")
            .check_module("lib.app", "from lib._extra import run"),
            expected=[
                NameFromPackageViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 24),
                    package="lib._extra",
                    name="run",
                    source=None,
                )
            ],
        ),
        # A package is rejected whatever the name; the missing name is ty's job.
        case(
            "reports nonexistent name in package",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib._core import missing"),
            expected=[
                NameFromPackageViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    package="lib._core",
                    name="missing",
                    source=None,
                )
            ],
        ),
        # The root package is a package too, and a way into an import cycle.
        case(
            "reports name from root package",
            Project()
            .package("lib", "from lib._wiring.greet import greet")
            .package("lib._wiring")
            .module("lib._wiring.greet", "def greet(): ...")
            .check_module("lib.app", "from lib import greet"),
            expected=[
                NameFromPackageViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 17),
                    package="lib",
                    name="greet",
                    source="lib._wiring.greet",
                )
            ],
        ),
        case(
            "reports package that shadows module with same name",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting", "def format_greeting(): ...")
            .package("lib._core.greeting")
            .check_module("lib.app", "from lib._core.greeting import format_greeting"),
            expected=[
                NameFromPackageViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 32),
                    package="lib._core.greeting",
                    name="format_greeting",
                    source=None,
                )
            ],
        ),
        case(
            "reports from-import in function",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .check_module(
                "lib.app",
                """
                def f():
                    from lib._core import greeting
                """,
            ),
            expected=[
                ModuleImportedAsNameViolation(
                    "src/lib/app.py", SourceLocation(2, 27), module="lib._core.greeting"
                )
            ],
        ),
        case(
            "passes name from top-level module",
            Project()
            .module("single", "def helper(): ...")
            .check_module("app", "from single import helper"),
            expected=[],
        ),
        case(
            "passes third-party packages",
            Project()
            .package("lib")
            .check_module(
                "lib.app",
                """
                from library import x
                from lib_extra.y import z
                from os import path
                """,
            ),
            expected=[],
        ),
        # Unresolved imports are ty's job.
        case(
            "passes nonexistent first-party module",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib._core.missing import x"),
            expected=[],
        ),
        # Relative imports are ruff's job (TID252); as absolute ones both names
        # would be reported.
        case(
            "passes relative import",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .package("lib._usecases")
            .check_module(
                "lib._usecases.app", "from .._core import greeting, format_greeting"
            ),
            expected=[],
        ),
        # Star imports are ruff's job (F403).
        case(
            "passes star import",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib._core import *"),
            expected=[],
        ),
    ],
)
def test_from_package_or_submodule(project, expected):
    assert check(project) == expected
