import tarfile
from collections.abc import Callable
from pathlib import Path

import pytest

CORPUS = Path(__file__).parent / "corpus" / "django-5.2.tar.xz"


def _make_module(n_classes: int, methods_per_class: int = 2) -> str:
    """Module of ``n_classes`` public classes with ``methods_per_class`` each."""
    lines = []
    for i in range(n_classes):
        lines.append(f"class C{i}:")
        lines.extend(
            f"    def m{j}(self, x):\n        return x + {j}"
            for j in range(methods_per_class)
        )
    return "\n".join(lines)


def _make_imports(n_imports: int) -> str:
    """Module of ``n_imports`` of each: plain, from and impure imports."""
    lines = []
    for i in range(n_imports):
        lines.append(f"import pkg{i}.sub")
        lines.append(f"from pkg{i} import a{i}, b{i}")
        lines.append(f"from os import getcwd as g{i}")
    return "\n".join(lines)


@pytest.fixture(scope="session")
def make_imports() -> Callable[..., str]:
    return _make_imports


@pytest.fixture(scope="session")
def make_module() -> Callable[..., str]:
    return _make_module


@pytest.fixture(scope="session")
def corpus_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The Django snapshot unpacked on disk."""
    root = tmp_path_factory.mktemp("corpus")
    with tarfile.open(CORPUS) as tar:
        tar.extractall(root, filter="data")
    return root / "django"


@pytest.fixture(scope="session")
def corpus(corpus_dir: Path) -> dict[str, str]:
    """``path -> source`` of every Python file in the Django snapshot."""
    return {
        str(path.relative_to(corpus_dir.parent)): path.read_text(encoding="utf-8")
        for path in sorted(corpus_dir.rglob("*.py"))
    }
