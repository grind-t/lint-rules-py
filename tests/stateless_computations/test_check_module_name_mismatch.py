from lint_rules._entities.violation_module_name_mismatch import (
    ViolationModuleNameMismatch,
)
from lint_rules._stateless_computations.check_module_name_mismatch import (
    check_module_name_mismatch,
)

_MATCHING = [
    ("parsed_file", "class ParsedFile: ..."),
    ("lint", "def lint(): ...\ndef helper(): ..."),
    ("limits", "LIMITS = 1"),
    ("check", "type Check = int"),
    ("http_server", "class HTTPServer: ..."),
]


def test_module_names(subtests, fake_project):
    cases = [
        fake_project.case(
            f"passes {name}.py with {source!r}",
            fake_project.project().check_module(name, source),
            expected=[],
        )
        for name, source in _MATCHING
    ] + [
        fake_project.case(
            "reports a module named after none of its public names",
            fake_project.project().check_module("stderr", "def report(): ..."),
            expected=[
                ViolationModuleNameMismatch("src/stderr.py", public_names=("report",))
            ],
        ),
        fake_project.case(
            "ignores imported and private names",
            fake_project.project().check_module(
                "path", "from os import path\ndef _path(): ...\ndef join(): ..."
            ),
            expected=[
                ViolationModuleNameMismatch("src/path.py", public_names=("join",))
            ],
        ),
        fake_project.case(
            "skips a module without public names",
            fake_project.project().check_module("app", "_x = 1"),
            expected=[],
        ),
        fake_project.case(
            "skips dunder modules",
            fake_project.project().check_package("app", "def main(): ..."),
            expected=[],
        ),
    ]
    for description, project, expected in cases:
        with subtests.test(description):
            assert fake_project.check(project, check_module_name_mismatch) == expected
