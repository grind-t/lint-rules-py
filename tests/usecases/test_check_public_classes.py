from lint_rules._core.violation import Violation
from lint_rules._usecases.check_public_classes import check_public_classes


def fake_read_files(files: dict[str, str]):
    """Port fake: any function with the right signature will do."""
    return lambda _roots: files.items()


def test_reports_module_with_two_public_classes():
    files = fake_read_files(
        {"a.py": "class A: ...\nclass B: ...", "b.py": "class C: ..."}
    )
    assert check_public_classes(files, ["src"]) == [
        Violation("a.py", "2 public classes (A, B); split them into separate modules")
    ]


def test_marker_disables_check():
    source = "# allow-multiple-public-classes\nclass A: ...\nclass B: ..."
    assert check_public_classes(fake_read_files({"a.py": source}), ["src"]) == []
