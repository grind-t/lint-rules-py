from lint_rules._entities.source_file import SourceFile
from lint_rules._stateless_workflows.lint import lint


def lint_paths(files: dict[str, str], root: str = "src") -> list[str]:
    violations = []
    lint(
        [
            SourceFile(root=root, path=path, source=source)
            for path, source in files.items()
        ],
        violations.append,
    )
    return [v.path for v in violations]


def test_runs_every_check_on_every_file():
    paths = lint_paths(
        {
            "_entities/a.py": "class A: ...\nclass B: ...",
            "b.py": "class B:\n    def run(self): ...",
            "c.py": "class C: ...",
        }
    )
    assert paths == ["_entities/a.py", "b.py"]


def test_runs_stateful_checks_across_files():
    paths = lint_paths(
        {
            "lib/__init__.py": "",
            "lib/a.py": "",
            "lib/b.py": "from lib import a",
        },
        root=".",
    )
    assert paths == ["lib/b.py"]
