from lint_rules._stateless_computations.qualified_module_name import (
    qualified_module_name,
)


def test_module_name_django(benchmark, corpus):
    benchmark(lambda: [qualified_module_name(path, "django") for path in corpus])
