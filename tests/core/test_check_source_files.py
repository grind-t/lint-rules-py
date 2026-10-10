from lint_rules._core.check_source_files import check_source_files
from lint_rules._core.source.source_file import SourceFile


def source_files(files: dict[str, str], root: str = "src") -> list[SourceFile]:
    return [SourceFile(root, path, source) for path, source in files.items()]


def test_runs_every_check_on_every_file():
    files = source_files(
        {
            "a.py": "class A: ...\nclass B: ...",
            "b.py": "class C:\n    def run(self): ...",
            "c.py": "class D: ...",
        }
    )
    assert [v.path for v in check_source_files(files)] == ["a.py", "b.py"]


def test_runs_stateful_checks_across_files():
    files = source_files(
        {
            "lib/__init__.py": "",
            "lib/a.py": "",
            "lib/b.py": "from lib import a",
        },
        root=".",
    )
    assert [v.path for v in check_source_files(files)] == ["lib/b.py"]
