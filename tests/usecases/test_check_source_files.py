from lint_rules._core.source_file import SourceFile
from lint_rules._usecases.check_source_files import check_source_files


def fake_read_files(files: dict[str, str]):
    """Port fake: any function with the right signature will do."""
    return lambda _roots: [
        SourceFile(".", path, source) for path, source in files.items()
    ]


def test_runs_every_check_on_every_file():
    files = fake_read_files(
        {
            "a.py": "class A: ...\nclass B: ...",
            "b.py": "class C:\n    def run(self): ...",
            "c.py": "class D: ...",
        }
    )
    assert [v.path for v in check_source_files(files, ["src"])] == ["a.py", "b.py"]
