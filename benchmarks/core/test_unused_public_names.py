import ast

from lint_rules._core.unused_public_names import (
    summarize_module,
    unused_public_names,
)


def test_summarize_module_django(benchmark, corpus):
    trees = [(path, ast.parse(source)) for path, source in corpus.items()]
    benchmark(lambda: [summarize_module(path, tree) for path, tree in trees])


def test_unused_public_names_django(benchmark, corpus):
    summaries = [
        summarize_module(path, ast.parse(source)) for path, source in corpus.items()
    ]
    benchmark(unused_public_names, summaries)
