from textwrap import dedent
from typing import Self

import pytest

from lint_rules._core.violation import Violation
from lint_rules._usecases.check_source_files import check_source_files


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

    @staticmethod
    def _package_path(name: str) -> str:
        return name.replace(".", "/") + "/__init__.py"

    @staticmethod
    def _module_path(name: str) -> str:
        return name.replace(".", "/") + ".py"


def check(project: Project) -> list[Violation]:
    """Violations of the checked file; other files only give context."""
    assert project.checked_path, "the project has no checked file"
    violations = check_source_files(lambda _roots: project.files.items(), ["src"])
    return [v for v in violations if v.path == project.checked_path]


def case(description: str, project: Project, *, expected: list[Violation]):
    return pytest.param(project, expected, id=description)
