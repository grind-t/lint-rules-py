import pytest
from fake_project import Project, case, check

from lint_rules._core.source.source_location import SourceLocation
from lint_rules._core.violations.reexported_module import ReexportedModuleViolation
from lint_rules._core.violations.reexported_name import ReexportedNameViolation


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
                ReexportedNameViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 26),
                    name="NameSource",
                    module="lib.greeting",
                    source="lib.name_source",
                    source_name="NameSource",
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
                ReexportedNameViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    name="nullcontext",
                    module="lib.names",
                    source="contextlib",
                    source_name="nullcontext",
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
                ReexportedNameViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    name="quiet",
                    module="lib.names",
                    source="contextlib",
                    source_name="suppress",
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
                ReexportedModuleViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    name="sys",
                    module="lib.names",
                    imported="sys",
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
                ReexportedModuleViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    name="os",
                    module="lib.names",
                    imported="os",
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
                ReexportedModuleViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    name="osp",
                    module="lib.names",
                    imported="os.path",
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
                ReexportedNameViolation(
                    "src/lib/app.py",
                    SourceLocation(1, 23),
                    name="greet",
                    module="lib.names",
                    source=None,
                    source_name="greet",
                )
            ],
        ),
    ],
)
def test_name_must_be_defined_in_module(project, expected):
    assert check(project) == expected
