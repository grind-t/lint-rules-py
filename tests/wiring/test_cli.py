from lint_rules import main


def test_cli_fails_on_violation(tmp_path, capsys):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "bad.py").write_text("class A: ...\nclass B: ...\n")
    (tmp_path / "ok.py").write_text("class A: ...\n")

    assert main([str(tmp_path)]) == 1
    assert capsys.readouterr().err == (
        f"{tmp_path / 'pkg' / 'bad.py'}: 2 public classes (A, B); "
        "split them into separate modules\n"
    )


def test_cli_passes_clean_tree(tmp_path, capsys):
    (tmp_path / "ok.py").write_text("class A: ...\n")

    assert main([str(tmp_path)]) == 0
    assert capsys.readouterr().err == ""
