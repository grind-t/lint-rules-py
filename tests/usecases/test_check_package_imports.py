import pytest
from fake_project import Project, case, check


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
                "line 1, col 23: lib._core.greeting is a module; "
                "import names from it instead of the module itself"
            ],
        ),
        case(
            "reports subpackage imported as name",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib import _core"),
            expected=[
                "line 1, col 17: lib._core is a module; "
                "import names from it instead of the module itself"
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
                "line 1, col 23: lib._core is a package; "
                "import format_greeting from lib._core.greeting"
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
                "line 2, col 5: lib._core is a package; "
                "import format_greeting from lib._core.greeting",
                "line 3, col 5: lib._core.greeting is a module; "
                "import names from it instead of the module itself",
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
                "line 1, col 23: lib._core is a package; "
                "move DEFAULT_NAME from its __init__.py to a module"
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
                "line 1, col 23: lib._core.greeting is a module; "
                "import names from it instead of the module itself"
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
                "line 1, col 24: lib._extra.plugin is a module; "
                "import names from it instead of the module itself"
            ],
        ),
        case(
            "reports name from namespace package",
            Project()
            .package("lib")
            .module("lib._extra.plugin", "def run(): ...")
            .check_module("lib.app", "from lib._extra import run"),
            expected=[
                "line 1, col 24: lib._extra is a package; "
                "import run from the module that defines it"
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
                "line 1, col 23: lib._core is a package; "
                "import missing from the module that defines it"
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
                "line 1, col 17: lib is a package; import greet from lib._wiring.greet"
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
                "line 1, col 32: lib._core.greeting is a package; "
                "import format_greeting from the module that defines it"
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
                "line 2, col 27: lib._core.greeting is a module; "
                "import names from it instead of the module itself"
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
    ],
)
def test_from_package_or_submodule(project, expected):
    assert check(project) == expected
