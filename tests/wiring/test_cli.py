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


def test_cli_reports_single_method_class(tmp_path, capsys):
    (tmp_path / "bad.py").write_text("class A:\n    def run(self): ...\n")

    assert main([str(tmp_path)]) == 1
    assert capsys.readouterr().err == (
        f"{tmp_path / 'bad.py'}: line 1: class A has a single method run; "
        "use a function, a Callable alias or a Protocol with __call__\n"
    )


def test_cli_passes_clean_tree(tmp_path, capsys):
    (tmp_path / "ok.py").write_text("class A: ...\n")

    assert main([str(tmp_path)]) == 0
    assert capsys.readouterr().err == ""


def test_cli_reports_unused_public_function(tmp_path, capsys):
    (tmp_path / "bad.py").write_text("def helper(): ...\n")

    assert main([str(tmp_path)]) == 1
    assert capsys.readouterr().err == (
        f"{tmp_path / 'bad.py'}: line 1: function helper is not used outside "
        "the module; rename it to _helper\n"
    )
