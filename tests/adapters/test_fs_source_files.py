from lint_rules._adapters.fs_source_files import read_fs_source_files
from lint_rules._core.source_file import SourceFile


def test_reads_python_files_recursively_in_sorted_order(tmp_path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "b.py").write_text("b = 1\n")
    (tmp_path / "a.py").write_text("a = 1\n")
    (tmp_path / "notes.txt").write_text("not python\n")

    assert list(read_fs_source_files([str(tmp_path)])) == [
        SourceFile(str(tmp_path), str(tmp_path / "a.py"), "a = 1\n"),
        SourceFile(str(tmp_path), str(tmp_path / "pkg" / "b.py"), "b = 1\n"),
    ]


def test_reads_every_root(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.py").write_text("")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "b.py").write_text("")

    roots = [str(tmp_path / "tests"), str(tmp_path / "src")]
    assert [(f.root, f.path) for f in read_fs_source_files(roots)] == [
        (str(tmp_path / "tests"), str(tmp_path / "tests" / "b.py")),
        (str(tmp_path / "src"), str(tmp_path / "src" / "a.py")),
    ]


def test_decodes_utf8(tmp_path):
    (tmp_path / "a.py").write_bytes("s = 'привет'\n".encode())

    assert list(read_fs_source_files([str(tmp_path)])) == [
        SourceFile(str(tmp_path), str(tmp_path / "a.py"), "s = 'привет'\n"),
    ]
