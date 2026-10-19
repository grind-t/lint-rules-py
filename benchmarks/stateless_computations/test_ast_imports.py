import ast

import pytest

from lint_rules._stateless_computations.ast_from_imports import ast_from_imports
from lint_rules._stateless_computations.ast_imports import ast_imports
from lint_rules._stateless_computations.ast_impure_imports import ast_impure_imports


@pytest.mark.parametrize("extract", [ast_imports, ast_from_imports, ast_impure_imports])
@pytest.mark.parametrize("n_imports", [10, 100, 1000])
def test_imports(benchmark, make_imports, extract, n_imports):
    benchmark(extract, ast.parse(make_imports(n_imports)))
