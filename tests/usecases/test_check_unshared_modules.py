from lint_rules._core.layout.unshared_module_violation import UnsharedModuleViolation
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_file import SourceFile
from lint_rules._usecases.check_unshared_modules import CheckUnsharedModules


def _check(files: dict[str, str]):
    check = CheckUnsharedModules("src")
    for path, source in files.items():
        check.visit(ParsedFile(SourceFile(path, source)))
    return check.finish()


def test_reports_module_used_by_one_feature():
    files = {
        "src/lib/shared/base.py": "",
        "src/lib/a/x.py": "from lib.shared.base import Base",
        "src/lib/b/y.py": "",
    }
    assert _check(files) == [
        UnsharedModuleViolation("src/lib/shared/base.py", features=("a",))
    ]
