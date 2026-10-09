import pytest

from lint_rules._composition_root.cli import main


def test_checks_the_given_root(tmp_path, capsys):
    (tmp_path / "a.py").write_text("class A: ...\nclass B: ...\n")

    assert main([str(tmp_path)]) == 1
    assert "a.py" in capsys.readouterr().err


def test_passes_clean_root(tmp_path):
    (tmp_path / "a.py").write_text("_x = 1\n")

    assert main([str(tmp_path)]) == 0


def test_rejects_more_than_one_root(tmp_path):
    with pytest.raises(SystemExit) as exit_info:
        main([str(tmp_path), str(tmp_path)])

    assert exit_info.value.code == 2
