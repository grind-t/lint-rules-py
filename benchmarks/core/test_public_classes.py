import ast

import pytest

from lint_rules._core.public_classes import public_classes


@pytest.mark.parametrize("n_classes", [10, 100, 1000])
def test_public_classes(benchmark, make_module, n_classes):
    benchmark(public_classes, ast.parse(make_module(n_classes)))


def test_exception_hierarchy(benchmark):
    """Worst case: every class extends the previous one and grows ``exempt``."""
    source = "class E0(Exception): ...\n" + "\n".join(
        f"class E{i}(E{i - 1}): ..." for i in range(1, 1000)
    )
    benchmark(public_classes, ast.parse(source))
