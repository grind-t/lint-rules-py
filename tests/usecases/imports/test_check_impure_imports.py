from fake_project import Project, case, check

from lint_rules._core.imports.impure_import_violation import ImpureImportViolation
from lint_rules._core.source.source_location import SourceLocation
from lint_rules._usecases.check_impure_imports import check_impure_imports


def test_impure_imports(subtests):
    cases = [
        case(
            "reports impure name in a no-I/O layer",
            Project().check_file("pkg/_core/a.py", "from pathlib import Path"),
            expected=[
                ImpureImportViolation(
                    "src/pkg/_core/a.py",
                    SourceLocation(1, 21),
                    statement="from pathlib import Path",
                )
            ],
        ),
        case(
            "reports plain import in a no-I/O layer",
            Project().check_file("pkg/_usecases/a.py", "import subprocess"),
            expected=[
                ImpureImportViolation(
                    "src/pkg/_usecases/a.py",
                    SourceLocation(1, 8),
                    statement="import subprocess",
                )
            ],
        ),
        case(
            "passes pure name in a no-I/O layer",
            Project().check_file("pkg/_core/a.py", "from pathlib import PurePosixPath"),
            expected=[],
        ),
        case(
            "passes impure name in an adapter",
            Project().check_file("pkg/_adapters/a.py", "from pathlib import Path"),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert check(project, check_impure_imports) == expected
