from lint_rules._core.violation import Violation
from lint_rules._usecases.check_public_classes import check_public_classes


class FakeSourceFiles:
    """Port fake: no inheritance, no mocks, just an object with the right method."""

    def __init__(self, files: dict[str, str]) -> None:
        self.files = files

    def read_all(self, roots):
        return self.files.items()


def test_reports_module_with_two_public_classes():
    files = FakeSourceFiles(
        {"a.py": "class A: ...\nclass B: ...", "b.py": "class C: ..."}
    )
    assert check_public_classes(files, ["src"]) == [
        Violation("a.py", "2 public classes (A, B); split them into separate modules")
    ]


def test_marker_disables_check():
    source = "# allow-multiple-public-classes\nclass A: ...\nclass B: ..."
    assert check_public_classes(FakeSourceFiles({"a.py": source}), ["src"]) == []
