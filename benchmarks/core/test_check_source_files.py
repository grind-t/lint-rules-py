from lint_rules._core.checks.check_source_files import check_source_files
from lint_rules._core.source.source_file import SourceFile


def test_check_source_files_django(benchmark, corpus):
    files = [SourceFile("django", path, source) for path, source in corpus.items()]
    benchmark(check_source_files, files)
