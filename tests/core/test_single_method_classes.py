import pytest

from lint_rules._core.single_method_classes import single_method_classes


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("class A:\n    def run(self): ...", [("A", "run", 1)]),
        ('class A:\n    """Doc."""\n    def run(self): ...', [("A", "run", 1)]),
        ("class A:\n    async def run(self): ...", [("A", "run", 1)]),
        ("class A:\n    @staticmethod\n    def run(): ...", [("A", "run", 1)]),
        ("class A:\n    def __call__(self): ...", [("A", "__call__", 1)]),
        ("class P(Protocol):\n    def run(self): ...", [("P", "run", 1)]),
        ("class P(typing.Protocol[T]):\n    def run(self): ...", [("P", "run", 1)]),
        ("class _A(object):\n    def run(self): ...", [("_A", "run", 1)]),
        ("def f():\n    class A:\n        def run(self): ...", [("A", "run", 2)]),
        ("class P(Protocol):\n    def __call__(self): ...", []),
        ("class A:\n    def run(self): ...\n    def stop(self): ...", []),
        ("class A:\n    def __init__(self): ...", []),
        ("class A:\n    def __init__(self, x): self.x = x\n    def run(self): ...", []),
        ("class A: ...", []),
        ("@dataclass\nclass A:\n    x: int\n    def run(self): ...", []),
        ("class A:\n    x = 1\n    def run(self): ...", []),
        ("class A(Base):\n    def run(self): ...", []),
        ("class A(metaclass=M):\n    def run(self): ...", []),
    ],
)
def test_single_method_classes(source, expected):
    assert single_method_classes(source) == expected
