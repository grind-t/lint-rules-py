import pytest
from fake_project import Project, case, check


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
                '1:1: relative import; use "from lib._core.greeting import ..." instead'
            ],
        ),
        case(
            "reports dot-only import with anchor package",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from . import greet"),
            expected=[
                '1:1: relative import; use "from lib._usecases import ..." instead'
            ],
        ),
        case(
            "reports import beyond top-level package without name",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from ... import x"),
            expected=["1:1: relative import; use an absolute import instead"],
        ),
        case(
            "resolves package __init__.py against the package itself",
            Project()
            .package("lib")
            .check_package("lib._core", "from .greeting import format_greeting"),
            expected=[
                '1:1: relative import; use "from lib._core.greeting import ..." instead'
            ],
        ),
        # Not importable, but still checked.
        case(
            "checks file without module name",
            Project().package("lib").check_file("my-dir/x.py", "from . import x"),
            expected=["1:1: relative import; use an absolute import instead"],
        ),
    ],
)
def test_relative_import(project, expected):
    assert check(project) == expected
