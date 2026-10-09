import ast

from lint_rules._core.imports.impure_imports import impure_imports
from lint_rules._core.source.source_location import SourceLocation


def test_impure_imports(subtests):
    cases = [
        ("from pathlib import Path", [("from pathlib import Path", (1, 21))]),
        (
            "from pathlib import PurePath, Path",
            [("from pathlib import Path", (1, 31))],
        ),
        ("from pathlib import PurePath, PurePosixPath", []),
        ("from io import open", [("from io import open", (1, 16))]),
        ("from io import StringIO, BytesIO", []),
        ("from os import environ", [("from os import environ", (1, 16))]),
        ("from os import path", [("from os import path", (1, 16))]),
        ("from os import fspath, PathLike", []),
        ("from os.path import exists", [("from os.path import exists", (1, 21))]),
        ("from os.path import join, basename", []),
        ("from subprocess import PIPE", [("from subprocess import PIPE", (1, 24))]),
        ("from socket import AF_INET", [("from socket import AF_INET", (1, 20))]),
        ("import pathlib", [("import pathlib", (1, 8))]),
        ("import os", [("import os", (1, 8))]),
        ("from json import loads", []),
    ]
    for source, expected in cases:
        with subtests.test(repr(source)):
            assert impure_imports(ast.parse(source)) == [
                (statement, SourceLocation(*location))
                for statement, location in expected
            ]
