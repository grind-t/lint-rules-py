import ast

import pytest


@pytest.mark.parametrize("n_classes", [10, 100, 1000])
def test_parse(benchmark, make_module, n_classes):
    """Baseline: each file is parsed once and the tree is shared by every rule."""
    benchmark(ast.parse, make_module(n_classes))
