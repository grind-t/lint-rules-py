from lint_rules._entities.source_file import SourceFile
from lint_rules._stateless_workflows.lint import lint


def test_lint_django(benchmark, corpus):
    files = [
        SourceFile(root="django", path=path, source=source)
        for path, source in corpus.items()
    ]
    benchmark(lint, files, lambda _: None)
