import ast

import pytest

from lint_rules._core.names.public_names import public_names


@pytest.mark.parametrize("n_classes", [10, 100, 1000])
def test_public_names(benchmark, make_module, n_classes):
    benchmark(public_names, ast.parse(make_module(n_classes)))
