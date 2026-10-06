from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)


def test_check_single_method_classes_django(benchmark, corpus):
    benchmark(check_single_method_classes, lambda _roots: corpus.items(), ["django"])
