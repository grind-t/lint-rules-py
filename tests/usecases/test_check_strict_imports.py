from textwrap import dedent
from typing import Self

import pytest

from lint_rules._usecases.check_source_files import check_source_files


class Project:
    """Files under the root "src", one of them checked.

    Modules and packages are named as in Python; nothing is created implicitly,
    so a directory without ``.package(...)`` has no __init__.py.
    """

    def __init__(self) -> None:
        self.files: dict[str, str] = {}
        self.checked_path = ""

    def package(self, name: str, source: str = "") -> Self:
        return self.file(self._package_path(name), source)

    def module(self, name: str, source: str = "") -> Self:
        return self.file(self._module_path(name), source)

    def file(self, path: str, source: str = "") -> Self:
        self.files[f"src/{path}"] = dedent(source).lstrip("\n")
        return self

    def check_package(self, name: str, source: str) -> Self:
        return self.check_file(self._package_path(name), source)

    def check_module(self, name: str, source: str) -> Self:
        return self.check_file(self._module_path(name), source)

    def check_file(self, path: str, source: str) -> Self:
        self.checked_path = f"src/{path}"
        return self.file(path, source)

    @staticmethod
    def _package_path(name: str) -> str:
        return name.replace(".", "/") + "/__init__.py"

    @staticmethod
    def _module_path(name: str) -> str:
        return name.replace(".", "/") + ".py"


def check(project: Project) -> list[str]:
    """Messages reported for the checked file; other files only give context."""
    assert project.checked_path, "the project has no checked file"
    violations = check_source_files(lambda _roots: project.files.items(), ["src"])
    return [v.message for v in violations if v.path == project.checked_path]


def case(description: str, project: Project, *, expected: list[str]):
    return pytest.param(project, expected, id=description)


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports root package",
            Project().package("lib").check_module("lib.app", "import lib"),
            expected=[
                'line 1, col 8: "import lib" '
                'binds a first-party module; use "from <module> import <name>" instead'
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
                'line 1, col 8: "import lib._core.greeting" '
                'binds a first-party module; use "from <module> import <name>" instead'
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
                'line 1, col 12: "import lib._core.greeting" '
                'binds a first-party module; use "from <module> import <name>" instead'
            ],
        ),
        # Only the first component matters; whether the module exists does not.
        case(
            "reports nonexistent first-party module",
            Project().package("lib").check_module("lib.app", "import lib._nope"),
            expected=[
                'line 1, col 8: "import lib._nope" '
                'binds a first-party module; use "from <module> import <name>" instead'
            ],
        ),
        case(
            "reports top-level module",
            Project().module("single").check_module("app", "import single"),
            expected=[
                'line 1, col 8: "import single" '
                'binds a first-party module; use "from <module> import <name>" instead'
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
                "line 1, col 26: NameSource is not defined in lib.greeting, "
                "only imported there; import NameSource from lib.name_source"
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
                "line 1, col 23: nullcontext is not defined in lib.names, "
                "only imported there; import nullcontext from contextlib"
            ],
        ),
        case(
            "reports re-export under alias",
            Project()
            .package("lib")
            .module("lib.names", "from contextlib import suppress as quiet")
            .check_module("lib.app", "from lib.names import quiet"),
            expected=[
                "line 1, col 23: quiet is not defined in lib.names, "
                "only imported there; import suppress from contextlib"
            ],
        ),
        case(
            "reports re-exported module",
            Project()
            .package("lib")
            .module("lib.names", "import sys")
            .check_module("lib.app", "from lib.names import sys"),
            expected=[
                "line 1, col 23: sys is not defined in lib.names, "
                "only imported there as module sys"
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
                "line 1, col 23: os is not defined in lib.names, "
                "only imported there as module os"
            ],
        ),
        case(
            "reports re-exported module alias",
            Project()
            .package("lib")
            .module("lib.names", "import os.path as osp")
            .check_module("lib.app", "from lib.names import osp"),
            expected=[
                "line 1, col 23: osp is not defined in lib.names, "
                "only imported there as module os.path"
            ],
        ),
        case(
            "reports re-exported relative import",
            Project()
            .package("lib")
            .module("lib.names", "from .greet import greet")
            .check_module("lib.app", "from lib.names import greet"),
            expected=[
                "line 1, col 23: greet is not defined in lib.names, "
                "only imported there; import it from the module that defines it"
            ],
        ),
    ],
)
def test_name_must_be_defined_in_module(project, expected):
    assert check(project) == expected


@pytest.mark.parametrize(
    ("project", "expected"),
    [
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
                'line 2, col 12: "import lib._core.greeting" '
                'binds a first-party module; use "from <module> import <name>" instead'
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
    ],
)
def test_import_location_does_not_matter(project, expected):
    assert check(project) == expected


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports def __getattr__",
            Project().check_module("app", "def __getattr__(name): ..."),
            expected=[
                "line 1, col 1: module-level __getattr__ makes names dynamic; "
                "define them explicitly"
            ],
        ),
        case(
            "reports __getattr__ assignment",
            Project().check_module("app", "__getattr__ = _lazy"),
            expected=[
                "line 1, col 1: module-level __getattr__ makes names dynamic; "
                "define them explicitly"
            ],
        ),
        # lib._lazy does not exist, so only the binding is reported.
        case(
            "reports imported __getattr__",
            Project()
            .package("lib")
            .check_module("lib.app", "from lib._lazy import __getattr__"),
            expected=[
                "line 1, col 23: module-level __getattr__ makes names dynamic; "
                "define them explicitly"
            ],
        ),
        case(
            "reports __getattr__ in top-level block",
            Project().check_module(
                "app",
                """
                if sys.version_info < (3, 15):
                    def __getattr__(name): ...
                """,
            ),
            expected=[
                "line 2, col 5: module-level __getattr__ makes names dynamic; "
                "define them explicitly"
            ],
        ),
        case(
            "passes __getattr__ method",
            Project().check_module(
                "app",
                """
                class C(Base):
                    def __getattr__(self, name): ...
                """,
            ),
            expected=[],
        ),
        case(
            "passes local __getattr__ function",
            Project().check_module(
                "app",
                """
                def f():
                    def __getattr__(name): ...
                """,
            ),
            expected=[],
        ),
        # __dir__ only affects dir() and adds no names.
        case(
            "passes __dir__",
            Project().check_module("app", "def __dir__(): ..."),
            expected=[],
        ),
    ],
)
def test_module_getattr(project, expected):
    assert check(project) == expected


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports with absolute module name",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module(
                "lib._usecases.app", "from .._core.greeting import format_greeting"
            ),
            expected=[
                "line 1, col 1: relative import; "
                'use "from lib._core.greeting import ..." instead'
            ],
        ),
        case(
            "reports dot-only import with anchor package",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from . import greet"),
            expected=[
                "line 1, col 1: relative import; "
                'use "from lib._usecases import ..." instead'
            ],
        ),
        # One violation per statement; its aliases are not checked further, though
        # as absolute imports both would be reported.
        case(
            "reports once per statement",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .package("lib._usecases")
            .check_module(
                "lib._usecases.app", "from .._core import greeting, format_greeting"
            ),
            expected=[
                "line 1, col 1: relative import; "
                'use "from lib._core import ..." instead'
            ],
        ),
        case(
            "reports star import only as relative",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from .._core import *"),
            expected=[
                "line 1, col 1: relative import; "
                'use "from lib._core import ..." instead'
            ],
        ),
        case(
            "reports import beyond top-level package without name",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from ... import x"),
            expected=["line 1, col 1: relative import; use an absolute import instead"],
        ),
        case(
            "reports __getattr__ binding separately",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from .lazy import __getattr__"),
            expected=[
                "line 1, col 1: relative import; "
                'use "from lib._usecases.lazy import ..." instead',
                "line 1, col 19: module-level __getattr__ makes names dynamic; "
                "define them explicitly",
            ],
        ),
        case(
            "resolves package __init__.py against the package itself",
            Project()
            .package("lib")
            .check_package("lib._core", "from .greeting import format_greeting"),
            expected=[
                "line 1, col 1: relative import; "
                'use "from lib._core.greeting import ..." instead'
            ],
        ),
        # Not importable, but still checked.
        case(
            "checks file without module name",
            Project()
            .package("lib")
            .check_file(
                "my-dir/x.py",
                """
                import lib
                from . import x
                """,
            ),
            expected=[
                'line 1, col 8: "import lib" '
                'binds a first-party module; use "from <module> import <name>" instead',
                "line 2, col 1: relative import; use an absolute import instead",
            ],
        ),
    ],
)
def test_relative_import(project, expected):
    assert check(project) == expected


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        case(
            "reports first-party module",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .check_module("lib.app", "from lib._core.greeting import *"),
            expected=[
                'line 1, col 32: "from lib._core.greeting import *" hides which names '
                "are used; import them explicitly"
            ],
        ),
        # Checked before the package rule: one violation, not two.
        case(
            "reports package only once",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib._core import *"),
            expected=[
                'line 1, col 23: "from lib._core import *" hides which names are used; '
                "import them explicitly"
            ],
        ),
        case(
            "passes third-party module",
            Project().check_module("app", "from os.path import *"),
            expected=[],
        ),
    ],
)
def test_star_import(project, expected):
    assert check(project) == expected


def test_current_directory_as_root():
    files = {"lib/__init__.py": "", "lib/x.py": "import lib"}
    violations = check_source_files(lambda _roots: files.items(), ["."])

    assert [(v.path, v.message) for v in violations] == [
        (
            "lib/x.py",
            'line 1, col 8: "import lib" '
            'binds a first-party module; use "from <module> import <name>" instead',
        )
    ]
