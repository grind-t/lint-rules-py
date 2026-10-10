from lint_rules._core.checks.imports.check_impure_imports import check_impure_imports
from lint_rules._core.imports.impure_import_violation import ImpureImportViolation
from lint_rules._core.source.source_location import SourceLocation


def test_impure_imports(subtests, fake_project):
    cases = [
        fake_project.case(
            "reports impure name in a no-I/O layer",
            fake_project.project().check_file(
                "pkg/_core/a.py", "from pathlib import Path"
            ),
            expected=[
                ImpureImportViolation(
                    "src/pkg/_core/a.py",
                    SourceLocation(1, 21),
                    statement="from pathlib import Path",
                )
            ],
        ),
        fake_project.case(
            "reports plain import in a no-I/O layer",
            fake_project.project().check_file("pkg/_core/a.py", "import subprocess"),
            expected=[
                ImpureImportViolation(
                    "src/pkg/_core/a.py",
                    SourceLocation(1, 8),
                    statement="import subprocess",
                )
            ],
        ),
        fake_project.case(
            "passes pure name in a no-I/O layer",
            fake_project.project().check_file(
                "pkg/_core/a.py", "from pathlib import PurePosixPath"
            ),
            expected=[],
        ),
        fake_project.case(
            "passes impure name in the shell",
            fake_project.project().check_file(
                "pkg/_shell/a.py", "from pathlib import Path"
            ),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert fake_project.check(project, check_impure_imports) == expected
