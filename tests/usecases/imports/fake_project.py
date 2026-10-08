from collections.abc import Iterable
from textwrap import dedent
from typing import Self

import pytest

from lint_rules._core.shared.violation import Violation
from lint_rules._core.source.parsed_file import ParsedFile
from lint_rules._core.source.source_file import SourceFile
from lint_rules._usecases.check_source_files import Check, StatefulCheck


class Project:
    """Files under the root "src", one of them checked.

    Modules and packages are named as in Python; nothing is created implicitly,
    so a directory without ``.package(...)`` has no __init__.py.
    """

    def __init__(self) -> None:
        self.files: dict[str, str] = {}
        self.checked_path = ""

    def package(self, name: str, source: str = "") -> Self:
        return self.file(self._package_path(name), source)

    def module(self, name: str, source: str = "") -> Self:
        return self.file(self._module_path(name), source)

    def file(self, path: str, source: str = "") -> Self:
        self.files[f"src/{path}"] = dedent(source).lstrip("\n")
        return self

    def check_package(self, name: str, source: str) -> Self:
        return self.check_file(self._package_path(name), source)

    def check_module(self, name: str, source: str) -> Self:
        return self.check_file(self._module_path(name), source)

    def check_file(self, path: str, source: str) -> Self:
        self.checked_path = f"src/{path}"
        return self.file(path, source)

    def to_files(self) -> list[ParsedFile]:
        return [
            ParsedFile(SourceFile("src", path, source))
            for path, source in self.files.items()
        ]

    @staticmethod
    def _package_path(name: str) -> str:
        return name.replace(".", "/") + "/__init__.py"

    @staticmethod
    def _module_path(name: str) -> str:
        return name.replace(".", "/") + ".py"


def check_files(
    files: Iterable[ParsedFile], rule: Check | StatefulCheck
) -> list[Violation]:
    """Run only this rule on the files."""
    if callable(rule):
        return [violation for file in files for violation in rule(file)]
    for file in files:
        rule.visit(file)
    return rule.finish()


def check(project: Project, rule: Check | StatefulCheck) -> list[Violation]:
    """Violations of the checked file; other files only give context."""
    assert project.checked_path, "the project has no checked file"
    violations = check_files(project.to_files(), rule)
    return [v for v in violations if v.path == project.checked_path]


def case(description: str, project: Project, *, expected: list[Violation]):
    return pytest.param(project, expected, id=description)
