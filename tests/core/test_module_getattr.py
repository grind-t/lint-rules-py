import symtable

import pytest

from lint_rules._core.module_getattr import binds_module_getattr


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("def __getattr__(name): ...", True),
        ("__getattr__ = _lazy", True),
        ("from lib import __getattr__", True),
        ("for __getattr__ in hooks: ...", True),
        ("print(__getattr__)", False),
        ("class C:\n    def __getattr__(self, name): ...", False),
        ("def f():\n    def __getattr__(name): ...", False),
        ("def __dir__(): ...", False),
    ],
)
def test_binds_module_getattr(source, expected):
    assert (
        binds_module_getattr(symtable.symtable(source, "<string>", "exec")) is expected
    )
