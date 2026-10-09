import ast

import pytest

from lint_rules._core.imports.from_imports import from_imports
from lint_rules._core.imports.imported_modules import imported_modules
from lint_rules._core.imports.impure_imports import impure_imports
from lint_rules._core.imports.plain_imports import plain_imports


@pytest.mark.parametrize(
    "extract", [plain_imports, from_imports, imported_modules, impure_imports]
)
@pytest.mark.parametrize("n_imports", [10, 100, 1000])
def test_imports(benchmark, make_imports, extract, n_imports):
    benchmark(extract, ast.parse(make_imports(n_imports)))
