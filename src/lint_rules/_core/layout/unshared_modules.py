from collections import defaultdict
from collections.abc import Mapping, Set

_SHARED = "shared"
_PACKAGE_INIT = "__init__.py"


def _owner(path: str) -> str | None:
    """Directory whose ``shared/`` holds the file: the nearest one above it."""
    parts = path.split("/")[:-1]
    if _SHARED not in parts:
        return None
    index = len(parts) - 1 - parts[::-1].index(_SHARED)
    return "/".join(parts[:index])


def _feature(path: str, owner: str) -> str | None:
    """Subdirectory of ``owner`` the file is in, if it is in one."""
    prefix = f"{owner}/" if owner else ""
    if not path.startswith(prefix):
        return None
    parts = path.removeprefix(prefix).split("/")
    return parts[0] if len(parts) > 1 else None


def _features_using(
    path: str, owner: str, importers: Mapping[str, Set[str]]
) -> set[str]:
    """Features of ``owner`` that import the file, directly or through shared/."""
    features: set[str] = set()
    seen = {path}
    stack = [path]
    while stack:
        for importer in importers[stack.pop()]:
            feature = _feature(importer, owner)
            if feature == _SHARED and importer not in seen:
                seen.add(importer)
                stack.append(importer)
            elif feature not in (None, _SHARED):
                features.add(feature)
    return features


def unshared_modules(
    imports: Mapping[str, Set[str]], modules: Mapping[str, str]
) -> list[tuple[str, tuple[str, ...]]]:
    """``(path, features)`` for every module in a ``shared/`` used by fewer than two.

    ``imports`` maps each file to the module names it imports and ``modules``
    maps module names to files. A feature is a sibling directory of
    ``shared/``; files outside them, such as importers from other packages,
    do not count. Package ``__init__.py`` files are not reported.
    """
    importers: defaultdict[str, set[str]] = defaultdict(set)
    for path, names in imports.items():
        for name in names:
            if (target := modules.get(name)) and target != path:
                importers[target].add(path)
    found = []
    for path in sorted(imports):
        owner = _owner(path)
        if owner is None or path.endswith(f"/{_PACKAGE_INIT}"):
            continue
        features = _features_using(path, owner, importers)
        if len(features) < 2:
            found.append((path, tuple(sorted(features))))
    return found
