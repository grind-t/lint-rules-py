import ast
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass

FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


@dataclass(frozen=True)
class ModuleSummary:
    """What a module defines and uses, enough to judge its functions later."""

    path: str
    candidates: tuple[tuple[str, int], ...]
    used_names: frozenset[str]
    star_imports: tuple[str, ...]


def _declared_all(tree: ast.Module) -> set[str]:
    """String names listed in ``__all__`` assignments at the top level."""
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign | ast.AugAssign) and node.value:
            targets, value = [node.target], node.value
        else:
            continue
        if not any(isinstance(t, ast.Name) and t.id == "__all__" for t in targets):
            continue
        if isinstance(value, ast.List | ast.Tuple | ast.Set):
            names.update(
                elt.value
                for elt in value.elts
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
            )
    return names


def _is_dunder(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def _candidates(path: str, tree: ast.Module) -> tuple[tuple[str, int], ...]:
    """Public top-level functions that are not exempt from the rule.

    Exempt are functions of ``__init__.py``, dunders, names in ``__all__`` and
    decorated functions, which frameworks call without naming them.
    """
    if path.replace("\\", "/").endswith("/__init__.py") or path == "__init__.py":
        return ()
    exported = _declared_all(tree)
    return tuple(
        (node.name, node.lineno)
        for node in tree.body
        if isinstance(node, FUNCTION_TYPES)
        and not node.name.startswith("_")
        and not node.decorator_list
        and node.name not in exported
    )


def summarize_module(path: str, tree: ast.Module) -> ModuleSummary:
    """Candidates of a module and the names it can reach in other modules.

    A function of another module is reachable either through an import
    (``from a import f``) or an attribute (``a.f``); bare names are ignored
    because they can only refer to another module's function after an import.
    """
    used: set[str] = set()
    star: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            used.add(node.attr)
        elif isinstance(node, ast.alias):
            used.add(node.name)
        elif (
            isinstance(node, ast.ImportFrom)
            and node.module
            and any(alias.name == "*" for alias in node.names)
        ):
            star.append(node.module)
    return ModuleSummary(path, _candidates(path, tree), frozenset(used), tuple(star))


def _matches_module(path: str, module: str) -> bool:
    """Whether ``path`` may be the file of ``module``, compared by its tail."""
    stem = path.replace("\\", "/").removesuffix(".py").removesuffix("/__init__")
    tail = module.replace(".", "/")
    return stem == tail or stem.endswith(f"/{tail}")


def unused_public_functions(
    summaries: Iterable[ModuleSummary],
) -> list[tuple[str, str, int]]:
    """``(path, function, line)`` for public functions no other module uses."""
    summaries = list(summaries)
    counts = Counter(name for s in summaries for name in s.used_names)
    star_imports = {module for s in summaries for module in s.star_imports}
    found = []
    for summary in summaries:
        if any(_matches_module(summary.path, m) for m in star_imports):
            continue
        found.extend(
            (summary.path, name, line)
            for name, line in summary.candidates
            if counts[name] - (name in summary.used_names) == 0
        )
    return sorted(found, key=lambda item: (item[0], item[2]))
