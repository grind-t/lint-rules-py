from lint_rules._core.layout.crowded_directory_violation import (
    CrowdedDirectoryViolation,
)
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_file import SourceFile
from lint_rules._usecases.layout.check_crowded_directories import (
    CheckCrowdedDirectories,
)


def _check(modules: int):
    paths = [f"src/lib/m{i}.py" for i in range(modules)]
    check = CheckCrowdedDirectories()
    for path in paths:
        check.visit(ParsedFile(SourceFile("src", path, "")))
    return check.finish()


def test_reports_directory_over_limit():
    assert _check(11) == [CrowdedDirectoryViolation("src/lib", modules=11, limit=10)]
