import pytest
from fake_project import Project, case, check


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
        case(
            "passes third-party module",
            Project().check_module("app", "from os.path import *"),
            expected=[],
        ),
    ],
)
def test_star_import(project, expected):
    assert check(project) == expected
