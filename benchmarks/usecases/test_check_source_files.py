from lint_rules._usecases.check_source_files import check_source_files


def test_check_source_files_django(benchmark, corpus):
    benchmark(check_source_files, lambda _roots: corpus.items(), ["django"])
