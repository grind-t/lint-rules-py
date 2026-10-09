from lint_rules._core.layout.crowded_directories import crowded_directories
from lint_rules._core.layout.unshared_modules import unshared_modules
from lint_rules._core.source.module_name import module_name


def test_module_name_django(benchmark, corpus):
    benchmark(lambda: [module_name(path, "django") for path in corpus])


def test_crowded_directories_django(benchmark, corpus):
    benchmark(crowded_directories, list(corpus), 10)


def test_unshared_modules_django(benchmark, corpus):
    """Cross-file graph walk: ``imports`` maps each file to a few module names."""
    modules = {module_name(path, "") or path: path for path in corpus}
    names = list(modules)
    imports = {
        path: {names[(i + k) % len(names)] for k in (1, 7, 31)}
        for i, path in enumerate(corpus)
    }
    benchmark(unshared_modules, imports, modules)
