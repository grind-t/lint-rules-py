import pytest
from fake_project import Project, case, check

from lint_rules._core.source_location import SourceLocation
from lint_rules._core.violation import Violation


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports re-exported first-party name",
            Project()
            .package("lib")
            .module("lib.greeting", "from lib.name_source import NameSource")
            .check_module("lib.app", "from lib.greeting import NameSource"),
            expected=[
                Violation(
                    "src/lib/app.py",
                    "NameSource is not defined in lib.greeting, "
                    "only imported there; import NameSource from lib.name_source",
                    SourceLocation(1, 26),
                )
            ],
        ),
        # An annotation without a value binds nothing; the ImportError is ty's job.
        case(
            "passes annotation without value",
            Project()
            .package("lib")
            .module("lib.greeting", "LIMIT: int")
            .check_module("lib.app", "from lib.greeting import LIMIT"),
            expected=[],
        ),
        case(
            "passes nonexistent name",
            Project()
            .package("lib")
            .module("lib.greeting")
            .check_module("lib.app", "from lib.greeting import nothing"),
            expected=[],
        ),
        # Imported in try and defined in except: the definition is enough.
        case(
            "passes name both imported and defined",
            Project()
            .package("lib")
            .module(
                "lib.compat",
                """
                try:
                    from tomllib import loads
                except ImportError:
                    def loads(s): ...
                """,
            )
            .check_module("lib.app", "from lib.compat import loads"),
            expected=[],
        ),
        case(
            "passes every kind of module-level binding",
            Project()
            .package("lib")
            .module(
                "lib.names",
                """
                from contextlib import nullcontext
                A, *B = 1, 2, 3
                X = Y = 0
                COUNT: int = 0
                COUNT += 1
                for ITEM in (): ...
                with nullcontext() as CTX: ...
                if (N := 1): ...
                try:
                    T = 1
                except Exception as EXC:
                    pass
                while False:
                    W = 1
                match ():
                    case [P, *Q]: ...
                async def ASYNC(): ...
                type ALIAS = int
                class K: ...
                """,
            )
            .check_module(
                "lib.app",
                """
                from lib.names import (
                    A, B, X, Y, COUNT, ITEM, CTX, N, T, EXC, W, P, Q, ASYNC, ALIAS, K,
                )
                """,
            ),
            expected=[],
        ),
        case(
            "passes function-local name",
            Project()
            .package("lib")
            .module(
                "lib.names",
                """
                def outer():
                    INNER = 1
                """,
            )
            .check_module("lib.app", "from lib.names import INNER"),
            expected=[],
        ),
        case(
            "passes class attribute",
            Project()
            .package("lib")
            .module(
                "lib.names",
                """
                class K:
                    ATTR = 1
                """,
            )
            .check_module("lib.app", "from lib.names import ATTR"),
            expected=[],
        ),
        # Binding the same name inside a function does not define it in the module.
        case(
            "reports re-export shadowed only inside function",
            Project()
            .package("lib")
            .module(
                "lib.names",
                """
                from contextlib import nullcontext
                def outer():
                    nullcontext = 1
                """,
            )
            .check_module("lib.app", "from lib.names import nullcontext"),
            expected=[
                Violation(
                    "src/lib/app.py",
                    "nullcontext is not defined in lib.names, "
                    "only imported there; import nullcontext from contextlib",
                    SourceLocation(1, 23),
                )
            ],
        ),
        case(
            "reports re-export under alias",
            Project()
            .package("lib")
            .module("lib.names", "from contextlib import suppress as quiet")
            .check_module("lib.app", "from lib.names import quiet"),
            expected=[
                Violation(
                    "src/lib/app.py",
                    "quiet is not defined in lib.names, "
                    "only imported there; import suppress from contextlib",
                    SourceLocation(1, 23),
                )
            ],
        ),
        case(
            "reports re-exported module",
            Project()
            .package("lib")
            .module("lib.names", "import sys")
            .check_module("lib.app", "from lib.names import sys"),
            expected=[
                Violation(
                    "src/lib/app.py",
                    "sys is not defined in lib.names, "
                    "only imported there as module sys",
                    SourceLocation(1, 23),
                )
            ],
        ),
        # "import os.path" binds os.
        case(
            "reports module bound by dotted import",
            Project()
            .package("lib")
            .module("lib.names", "import os.path")
            .check_module("lib.app", "from lib.names import os"),
            expected=[
                Violation(
                    "src/lib/app.py",
                    "os is not defined in lib.names, only imported there as module os",
                    SourceLocation(1, 23),
                )
            ],
        ),
        case(
            "reports re-exported module alias",
            Project()
            .package("lib")
            .module("lib.names", "import os.path as osp")
            .check_module("lib.app", "from lib.names import osp"),
            expected=[
                Violation(
                    "src/lib/app.py",
                    "osp is not defined in lib.names, "
                    "only imported there as module os.path",
                    SourceLocation(1, 23),
                )
            ],
        ),
        case(
            "reports re-exported relative import",
            Project()
            .package("lib")
            .module("lib.names", "from .greet import greet")
            .check_module("lib.app", "from lib.names import greet"),
            expected=[
                Violation(
                    "src/lib/app.py",
                    "greet is not defined in lib.names, "
                    "only imported there; import it from the module that defines it",
                    SourceLocation(1, 23),
                )
            ],
        ),
    ],
)
def test_name_must_be_defined_in_module(project, expected):
    assert check(project) == expected
