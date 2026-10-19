from lint_rules._entities.impure_import_violation import ImpureImportViolation
from lint_rules._entities.source_location import SourceLocation
from lint_rules._stateless_computations.check_impure_imports import check_impure_imports


def test_impure_imports(subtests, fake_project):
    cases = [
        fake_project.case(
            "reports impure name in a no-I/O layer",
            fake_project.project().check_file(
                "pkg/_stateless_computations/a.py", "from pathlib import Path"
            ),
            expected=[
                ImpureImportViolation(
                    "src/pkg/_stateless_computations/a.py",
                    SourceLocation(1, 21),
                    statement="from pathlib import Path",
                )
            ],
        ),
        fake_project.case(
            "reports plain import in a no-I/O layer",
            fake_project.project().check_file(
                "pkg/_stateless_computations/a.py", "import subprocess"
            ),
            expected=[
                ImpureImportViolation(
                    "src/pkg/_stateless_computations/a.py",
                    SourceLocation(1, 8),
                    statement="import subprocess",
                )
            ],
        ),
        fake_project.case(
            "passes pure name in a no-I/O layer",
            fake_project.project().check_file(
                "pkg/_stateless_computations/a.py", "from pathlib import PurePosixPath"
            ),
            expected=[],
        ),
        fake_project.case(
            "passes impure name in effects",
            fake_project.project().check_file(
                "pkg/_stateful_effects/a.py", "from pathlib import Path"
            ),
            expected=[],
        ),
        *(
            fake_project.case(
                f"reports impure name in {layer}",
                fake_project.project().check_file(
                    f"pkg/{layer}/a.py", "import subprocess"
                ),
                expected=[
                    ImpureImportViolation(
                        f"src/pkg/{layer}/a.py",
                        SourceLocation(1, 8),
                        statement="import subprocess",
                    )
                ],
            )
            for layer in (
                "_entities",
                "_stateful_computations",
                "_stateless_workflows",
                "_stateful_workflows",
            )
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert fake_project.check(project, check_impure_imports) == expected
