from lint_rules._stateless_computations.module_name import module_name


def test_module_name_django(benchmark, corpus):
    benchmark(lambda: [module_name(path, "django") for path in corpus])
