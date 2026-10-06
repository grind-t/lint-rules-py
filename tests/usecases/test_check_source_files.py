from lint_rules._usecases.check_source_files import check_source_files


def fake_read_files(files: dict[str, str]):
    """Port fake: any function with the right signature will do."""
    return lambda _roots: files.items()


def test_runs_every_check_on_every_file():
    files = fake_read_files(
        {
            "a.py": "class A: ...\nclass B: ...",
            "b.py": "class C:\n    def run(self): ...",
            "c.py": "class D: ...",
        }
    )
    assert [v.path for v in check_source_files(files, ["src"])] == ["a.py", "b.py"]


def test_runs_stateful_checks_after_every_file():
    files = fake_read_files(
        {
            "a.py": "def helper(): ...\ndef used(): ...",
            "b.py": "from a import used\nclass A: ...\nclass B: ...",
        }
    )
    assert [str(v) for v in check_source_files(files, ["src"])] == [
        "b.py: 2 public classes (A, B); split them into separate modules",
        "a.py: line 1: function helper is not used outside the module; "
        "rename it to _helper",
    ]


def test_stateful_checks_start_fresh_on_every_run():
    files = fake_read_files({"a.py": "def helper(): ..."})
    assert check_source_files(files, ["src"]) == check_source_files(files, ["src"])
