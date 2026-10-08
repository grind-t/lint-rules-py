import ast

import pytest

from lint_rules._core.classes.single_method_classes import single_method_classes


@pytest.mark.parametrize("n_classes", [10, 100, 1000])
def test_single_method_classes(benchmark, make_module, n_classes):
    benchmark(single_method_classes, ast.parse(make_module(n_classes)))


def test_nested_classes(benchmark):
    """Worst case: the walk descends through deeply nested classes."""
    depth = 90  # the tokenizer allows at most 100 indentation levels
    nested = "\n".join(
        f"{'    ' * level}class C{level}:\n{'    ' * (level + 1)}def m(self): ..."
        for level in range(depth)
    )
    benchmark(single_method_classes, ast.parse("\n".join([nested] * 10)))
