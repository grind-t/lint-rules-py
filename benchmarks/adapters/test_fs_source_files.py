from lint_rules._adapters.fs_source_files import read_fs_source_files


def test_read_fs_source_files_django(benchmark, corpus_dir):
    """Measures ``rglob`` and reads from a warm OS page cache, not cold disk I/O."""
    benchmark(lambda: list(read_fs_source_files(str(corpus_dir))))
