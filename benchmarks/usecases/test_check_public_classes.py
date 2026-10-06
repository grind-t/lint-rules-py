from lint_rules._usecases.check_public_classes import check_public_classes


def test_check_public_classes_django(benchmark, corpus):
    benchmark(check_public_classes, lambda _roots: corpus.items(), ["django"])
