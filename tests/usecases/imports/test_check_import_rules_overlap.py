"""Imports that more than one import rule could report."""

import pytest
from fake_project import Project, case, check


@pytest.mark.parametrize(
    ("project", "expected"),
    [
        # One violation per statement; its aliases are not checked further, though
        # as absolute imports both would be reported.
        case(
            "reports relative import once per statement",
            Project()
            .package("lib")
            .package("lib._core")
            .module("lib._core.greeting")
            .package("lib._usecases")
            .check_module(
                "lib._usecases.app", "from .._core import greeting, format_greeting"
            ),
            expected=['1:1: relative import; use "from lib._core import ..." instead'],
        ),
        case(
            "reports relative star import only as relative",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from .._core import *"),
            expected=['1:1: relative import; use "from lib._core import ..." instead'],
        ),
        case(
            "reports __getattr__ binding separately from relative import",
            Project()
            .package("lib")
            .package("lib._usecases")
            .check_module("lib._usecases.app", "from .lazy import __getattr__"),
            expected=[
                "1:1: relative import; "
                'use "from lib._usecases.lazy import ..." instead',
                "module-level __getattr__ makes names dynamic; define them explicitly",
            ],
        ),
        # The star import is reported instead of the package: one violation, not two.
        case(
            "reports star import from package only once",
            Project()
            .package("lib")
            .package("lib._core")
            .check_module("lib.app", "from lib._core import *"),
            expected=[
                '1:23: "from lib._core import *" hides which names are used; '
                "import them explicitly"
            ],
        ),
    ],
)
def test_import_rules_overlap(project, expected):
    assert check(project) == expected
