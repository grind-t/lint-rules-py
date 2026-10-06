import ast

import pytest

from lint_rules._core.unused_public_functions import (
    summarize_module,
    unused_public_functions,
)


def unused(files: dict[str, str]) -> list[tuple[str, str, int]]:
    return unused_public_functions(
        summarize_module(path, ast.parse(source)) for path, source in files.items()
    )


def test_reports_function_used_only_inside_its_module():
    files = {"a.py": "x = 1\n\ndef helper(): ...\nhelper()"}
    assert unused(files) == [("a.py", "helper", 3)]


def test_reports_async_function():
    assert unused({"a.py": "async def run(): ..."}) == [("a.py", "run", 1)]


@pytest.mark.parametrize(
    "usage",
    [
        "from a import helper",
        "from a import helper as h",
        "from .a import helper",
        "import a\na.helper()",
        "import pkg.a as m\nm.helper",
    ],
)
def test_passes_function_used_by_another_module(usage):
    assert unused({"a.py": "def helper(): ...", "b.py": usage}) == []


def test_own_attribute_access_does_not_count():
    files = {"a.py": "import a\n\ndef helper(): ...\na.helper()"}
    assert unused(files) == [("a.py", "helper", 3)]


@pytest.mark.parametrize(
    "source",
    [
        "def _helper(): ...",
        "def __getattr__(name): ...",
        "@cache\ndef helper(): ...",
        "__all__ = ['helper']\ndef helper(): ...",
        "__all__: list[str] = ['helper']\ndef helper(): ...",
        "__all__ = []\n__all__ += ('helper',)\ndef helper(): ...",
        "class A:\n    def helper(self): ...",
        "def outer():\n    def helper(): ...\n    return helper()",
    ],
)
def test_ignores_exempt_and_non_top_level_functions(source):
    assert unused({"a.py": source, "b.py": "import a\na.outer()"}) == []


def test_ignores_functions_of_package_init():
    assert unused({"pkg/__init__.py": "def helper(): ..."}) == []


@pytest.mark.parametrize(
    ("path", "star"),
    [
        ("pkg/a.py", "from pkg.a import *"),
        ("pkg/a.py", "from .a import *"),
        ("src/pkg/a/__init__.py", "from pkg.a import *"),
    ],
)
def test_star_import_uses_every_function_of_module(path, star):
    assert unused({path: "def helper(): ...", "b.py": star}) == []


def test_star_import_of_other_module_does_not_count():
    files = {"pkg/a.py": "def helper(): ...", "b.py": "from pkg.ba import *"}
    assert unused(files) == [("pkg/a.py", "helper", 1)]


def test_sorts_by_path_and_line():
    files = {"b.py": "def g(): ...\ndef f(): ...", "a.py": "def h(): ..."}
    assert unused(files) == [("a.py", "h", 1), ("b.py", "g", 1), ("b.py", "f", 2)]


# Known false negatives: names are matched without resolving modules, so
# another module's import or attribute with the same name hides the function.


def test_known_false_negative_same_name_imported_from_elsewhere():
    files = {
        "a.py": "def helper(): ...\nhelper()",
        "b.py": "from c import helper",
        "c.py": "def helper(): ...",
    }
    assert ("a.py", "helper", 1) not in unused(files)


def test_known_false_negative_same_name_as_attribute():
    files = {
        "config.py": "def get(key): ...\nget('x')",
        "views.py": "request.GET.get('q')",
    }
    assert unused(files) == []


def test_known_false_positive_getattr_by_string():
    # Dynamic access is invisible; such modules need the marker.
    files = {"a.py": "def helper(): ...", "b.py": "import a\ngetattr(a, 'helper')"}
    assert unused(files) == [("a.py", "helper", 1)]
