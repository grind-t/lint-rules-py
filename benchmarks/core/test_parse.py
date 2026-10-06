import ast

import pytest


@pytest.mark.parametrize("n_classes", [10, 100, 1000])
def test_parse(benchmark, make_module, n_classes):
    """Baseline: every rule pays for ``ast.parse`` on its own."""
    benchmark(ast.parse, make_module(n_classes))
