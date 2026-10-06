import ast

import pytest

from lint_rules._core.candidate import Kind
from lint_rules._core.unused_public_names import (
    summarize_module,
    unused_public_names,
)


def unused(
    files: dict[str, str], kind: Kind = "function"
) -> list[tuple[str, str, int]]:
    found = unused_public_names(
        summarize_module(path, ast.parse(source)) for path, source in files.items()
    )
    return [(path, c.name, c.line) for path, c in found if c.kind == kind]


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


def test_same_name_imported_from_another_module_does_not_count():
    files = {
        "a.py": "def helper(): ...\nhelper()",
        "b.py": "from c import helper",
        "c.py": "def helper(): ...",
    }
    assert unused(files) == [("a.py", "helper", 1)]


def test_same_name_imported_from_outside_does_not_count():
    files = {"a.py": "def find(): ...", "b.py": "from ctypes.util import find"}
    assert unused(files) == [("a.py", "find", 1)]


def test_same_name_attribute_of_other_module_does_not_count():
    files = {
        "pkg/a.py": "def helper(): ...",
        "pkg/c.py": "",
        "b.py": "import pkg.c\npkg.c.helper()",
    }
    assert unused(files) == [("pkg/a.py", "helper", 1)]


@pytest.mark.parametrize(
    "usage",
    [
        "from pkg import a\na.helper()",
        "from ..pkg import a\na.helper()",
        "import pkg.a\npkg.a.helper()",
    ],
)
def test_attribute_resolved_through_import(usage):
    files = {"pkg/a.py": "def helper(): ...", "other/b.py": usage}
    assert unused(files) == []


@pytest.mark.parametrize(
    "usage",
    [
        # A module re-exported under another name is not a file.
        "import pkg\npkg.api.helper()",
        # Neither is an object that forwards attributes to a module.
        "from pkg.registry import proxy\nproxy.helper()",
    ],
)
def test_attribute_of_unknown_module_counts_by_name(usage):
    files = {
        "pkg/__init__.py": "from . import impl as api",
        "pkg/impl.py": "def helper(): ...",
        "b.py": usage,
    }
    assert unused(files) == []


def test_import_above_root_counts_by_name():
    files = {"a.py": "def helper(): ...", "pkg/b.py": "from ...x import helper"}
    assert unused(files) == []


@pytest.mark.parametrize(
    "usage",
    [
        "def _run(c):\n    c.helper()\n_run(a)",
        "def _run(*, c=a):\n    c.helper()",
        "(lambda c: c.helper())(a)",
        "def _run():\n    c = a\n    c.helper()",
        "def _run():\n    c.helper()\n    c = a",
        "def _run():\n    for c in [a]:\n        c.helper()",
        "def _run():\n    with nullcontext(a) as c:\n        c.helper()",
        "def _run():\n    try: ...\n    except Exception as c:\n        c.helper()",
        "def _run(x):\n    match x:\n        case [*c]:\n            c.helper()",
        "[c.helper() for c in [a]]",
        "def _run():\n    def c(): ...\n    c.helper()",
        "def _run(c):\n    def inner():\n        c.helper()",
    ],
)
def test_import_shadowed_by_local_name_counts_by_name(usage):
    files = {
        "a.py": "def helper(): ...",
        "c.py": "",
        "b.py": f"import a\nimport c\n\n{usage}",
    }
    assert unused(files) == []


@pytest.mark.parametrize(
    "usage",
    [
        "def _run(c): ...\nc.helper()",
        "def _run(xs):\n    [c for c in xs]\n    c.helper()",
        "def _run():\n    global c\n    c.helper()",
        "def _run():\n    import c\n    c.helper()",
    ],
)
def test_local_name_does_not_shadow_import_outside_its_scope(usage):
    files = {"a.py": "def helper(): ...", "c.py": "", "b.py": f"import c\n{usage}"}
    assert unused(files) == [("a.py", "helper", 1)]


# Known false negatives: an attribute of an object of unknown type counts by
# its bare name, so it hides any function with the same name.


def test_known_false_negative_same_name_as_attribute():
    files = {
        "config.py": "def get(key): ...\nget('x')",
        "views.py": "request.GET.get('q')",
    }
    assert unused(files) == []


# Known false positives: dynamic access is invisible, and rebinding an import
# counts only inside functions, lambdas and comprehensions. Such modules need
# the marker.


def test_known_false_positive_getattr_by_string():
    files = {"a.py": "def helper(): ...", "b.py": "import a\ngetattr(a, 'helper')"}
    assert unused(files) == [("a.py", "helper", 1)]


def test_known_false_positive_import_rebound_at_module_level():
    files = {
        "a.py": "def helper(): ...",
        "c.py": "",
        "b.py": "import a\nimport c\n\nc = a\nc.helper()",
    }
    assert unused(files) == [("a.py", "helper", 1)]


def test_reports_variable_used_only_inside_its_module():
    files = {"a.py": "def helper(): ...\nLIMIT = 1\nhelper(LIMIT)"}
    assert unused(files, "variable") == [("a.py", "LIMIT", 2)]


@pytest.mark.parametrize(
    ("source", "names"),
    [
        ("a, *b = c", ["a", "b"]),
        ("[a, (b, c)] = d", ["a", "b", "c"]),
        ("a = b = 1", ["a", "b"]),
        ("a: int = 1", ["a"]),
    ],
)
def test_reports_every_assigned_variable(source, names):
    assert unused({"m.py": source}, "variable") == [("m.py", n, 1) for n in names]


@pytest.mark.parametrize(
    "usage",
    [
        "from a import LIMIT",
        "from .a import LIMIT as L",
        "import a\nprint(a.LIMIT)",
        "import a\na.LIMIT = 2",
    ],
)
def test_passes_variable_used_by_another_module(usage):
    assert unused({"a.py": "LIMIT = 1", "b.py": usage}, "variable") == []


@pytest.mark.parametrize(
    "source",
    [
        "_limit = 1",
        "__version__ = '1.0'",
        "__all__ = ['LIMIT']\nLIMIT = 1",
        "LIMIT: int",
        "def f():\n    limit = 1",
        "class A:\n    LIMIT = 1",
        "if x:\n    LIMIT = 1",
        "type Alias = int",
    ],
)
def test_ignores_exempt_and_non_top_level_variables(source):
    assert unused({"a.py": source}, "variable") == []


def test_augmented_assignment_does_not_define_variable():
    files = {"a.py": "LIMIT = 0\nLIMIT += 1"}
    assert unused(files, "variable") == [("a.py", "LIMIT", 1)]


def test_name_defined_twice_is_reported_once():
    files = {"a.py": "LIMIT = 1\nLIMIT = 2\ndef LIMIT(): ..."}
    assert unused(files, "variable") == [("a.py", "LIMIT", 1)]
    assert unused(files, "function") == []


def test_variables_of_init_are_exempt():
    assert unused({"pkg/__init__.py": "LIMIT = 1"}, "variable") == []
