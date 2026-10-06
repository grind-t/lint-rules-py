from lint_rules._core.violation import Violation
from lint_rules._usecases.check_single_method_classes import (
    check_single_method_classes,
)


def fake_read_files(files: dict[str, str]):
    """Port fake: any function with the right signature will do."""
    return lambda _roots: files.items()


def test_reports_class_with_single_method():
    files = fake_read_files(
        {
            "a.py": "x = 1\n\nclass A:\n    def run(self): ...",
            "b.py": "def run(): ...",
        }
    )
    assert check_single_method_classes(files, ["src"]) == [
        Violation(
            "a.py",
            "line 3: class A has a single method run; "
            "use a function, a Callable alias or a Protocol with __call__",
        )
    ]


def test_marker_disables_check():
    source = "# allow-single-method-classes\nclass A:\n    def run(self): ..."
    files = fake_read_files({"a.py": source})
    assert check_single_method_classes(files, ["src"]) == []
