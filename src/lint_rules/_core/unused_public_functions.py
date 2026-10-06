import ast
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from importlib.util import resolve_name

# Not an identifier, so no module name can clash with it.
ROOT = "<root>"
FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
NAMED_BINDING_TYPES = (
    *FUNCTION_TYPES,
    ast.ClassDef,
    ast.ExceptHandler,
    ast.MatchAs,
    ast.MatchStar,
)
# AST classes are never subclassed, so hot loops look up the exact type rather
# than check ``isinstance`` against each one.
BINDING_KINDS = frozenset({ast.arg, ast.Name, ast.MatchMapping, *NAMED_BINDING_TYPES})
SCOPE_KINDS = frozenset(
    {
        *FUNCTION_TYPES,
        ast.Lambda,
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
    }
)


@dataclass(frozen=True)
class ModuleSummary:
    """What a module defines and uses, enough to judge its functions later.

    Usages are kept as qualified names (``module.function``) where the module
    is known from an import, and as bare names where it is not.
    """

    path: str
    candidates: tuple[tuple[str, int], ...]
    imported: frozenset[str]
    referenced: frozenset[str]
    attributes: frozenset[str]
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


def _package(path: str) -> list[str]:
    """Dotted parts of the package that relative imports in ``path`` start from."""
    parts = [part for part in path.replace("\\", "/").split("/") if part]
    return parts[:-1]


def _absolute_module(package: list[str], node: ast.ImportFrom) -> str | None:
    """Module of ``from ... import``, or ``None`` if it climbs above the root.

    ``resolve_name`` stops at the top package, while imports here may climb
    to the directory the paths start from, so it gets that as a package too.
    """
    name = "." * node.level + (node.module or "")
    try:
        module = resolve_name(name, ".".join([ROOT, *package]))
    except ImportError:
        return None
    return module.removeprefix(ROOT).removeprefix(".") or None


def _chain(node: ast.Attribute) -> list[str] | None:
    """``["a", "b", "f"]`` for ``a.b.f``, ``None`` unless it starts with a name."""
    parts: list[str] = []
    current: ast.expr = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if not isinstance(current, ast.Name):
        return None
    parts.append(current.id)
    return parts[::-1]


def _root(node: ast.Attribute) -> str | None:
    """``a`` for ``a.b.f``, ``None`` unless it starts with a name."""
    current = node.value
    while isinstance(current, ast.Attribute):
        current = current.value
    return current.id if isinstance(current, ast.Name) else None


def _bound_name(node: ast.AST) -> str | None:
    """Name that ``node`` of ``BINDING_KINDS`` binds, if any (imports aside)."""
    if isinstance(node, ast.Name):
        return node.id if isinstance(node.ctx, ast.Store | ast.Del) else None
    if isinstance(node, ast.arg):
        return node.arg
    if isinstance(node, ast.MatchMapping):
        return node.rest
    if isinstance(node, NAMED_BINDING_TYPES):
        return node.name
    return None


@dataclass
class _Scope:
    """Names a function, lambda or comprehension binds, and attributes in it.

    ``shadowed`` holds the imports rebound here or in an enclosing scope.
    """

    parent: _Scope | None
    bound: set[str | None] = field(default_factory=set)
    declared: set[str] = field(default_factory=set)
    attributes: list[tuple[ast.Attribute, str]] = field(default_factory=list)
    shadowed: set[str] = field(default_factory=set)


def _shadowed_attributes(tree: ast.Module, names: set[str]) -> set[ast.Attribute]:
    """Attributes on one of ``names`` inside a scope that rebinds that name.

    A name is bound for its whole scope, so scopes are collected in one walk
    and resolved after it. Bindings of the module and of class bodies do not
    count. Names of the enclosing scope used by a scope (defaults, decorators,
    the first iterable) are taken as its own, which only makes their
    attributes count by bare name.
    """
    module = _Scope(None)
    scopes = [module]
    stack: list[tuple[ast.AST, _Scope]] = [(tree, module)]
    while stack:
        node, scope = stack.pop()
        if type(node) is ast.Attribute:
            root = _root(node)
            if root in names:
                scope.attributes.append((node, root))
        elif type(node) in BINDING_KINDS:
            scope.bound.add(_bound_name(node))
        elif isinstance(node, ast.Global | ast.Nonlocal):
            scope.declared.update(node.names)
        if type(node) in SCOPE_KINDS:
            scope = _Scope(scope)
            scopes.append(scope)
        stack.extend([(child, scope) for child in ast.iter_child_nodes(node)])
    found: set[ast.Attribute] = set()
    for scope in scopes:  # Parents come before their children.
        if scope.parent:
            own = names.intersection(scope.bound) - scope.declared
            scope.shadowed = scope.parent.shadowed | own
        found.update(n for n, name in scope.attributes if name in scope.shadowed)
    return found


def summarize_module(path: str, tree: ast.Module) -> ModuleSummary:
    """Candidates of a module and the functions it can reach in other modules.

    A function of another module is reachable either through an import
    (``from a import f``) or an attribute (``a.f``); bare names are ignored
    because they can only refer to another module's function after an import.
    Attributes are resolved through the module's imports, unless a function,
    lambda or comprehension rebinds the name; the rest (``obj.f``) keep only
    the bare name.
    """
    package = _package(path)
    aliases: dict[str, str] = {}
    imported: set[str] = set()
    attributes: set[str] = set()
    star: list[str] = []
    chains: list[ast.Attribute] = []
    bound: set[str | None] = set()
    for node in ast.walk(tree):
        if type(node) is ast.Name:
            if type(node.ctx) is not ast.Load:
                bound.add(node.id)
        elif type(node) is ast.Attribute:
            chains.append(node)
        elif type(node) is ast.Import:
            for alias in node.names:
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    root = alias.name.partition(".")[0]
                    aliases[root] = root
        elif type(node) is ast.ImportFrom:
            module = _absolute_module(package, node)
            for alias in node.names:
                if alias.name == "*":
                    if module:
                        star.append(module)
                elif module is None:
                    attributes.add(alias.name)
                else:
                    imported.add(f"{module}.{alias.name}")
                    aliases[alias.asname or alias.name] = f"{module}.{alias.name}"
        elif type(node) in BINDING_KINDS:
            bound.add(_bound_name(node))
    # Rebinding an import is rare, so scopes are only walked when it happens.
    rebound = {
        root
        for node in chains
        if (root := _root(node)) is not None and root in aliases and root in bound
    }
    shadowed = _shadowed_attributes(tree, rebound) if rebound else set()
    referenced: set[str] = set()
    for node in chains:
        chain = _chain(node)
        if chain and chain[0] in aliases and node not in shadowed:
            referenced.add(".".join([aliases[chain[0]], *chain[1:]]))
        else:
            attributes.add(node.attr)
    return ModuleSummary(
        path,
        _candidates(path, tree),
        frozenset(imported),
        frozenset(referenced),
        frozenset(attributes),
        tuple(star),
    )


def _module_stem(path: str) -> str:
    return path.replace("\\", "/").removesuffix(".py").removesuffix("/__init__")


def _matches_module(path: str, module: str) -> bool:
    """Whether ``path`` may be the file of ``module``, compared by its tail."""
    stem = _module_stem(path)
    tail = module.replace(".", "/")
    return stem == tail or stem.endswith(f"/{tail}")


def _module_tails(paths: Iterable[str]) -> set[str]:
    """Every module name some path may be the file of (see ``_matches_module``)."""
    tails = set()
    for path in paths:
        parts = _module_stem(path).split("/")
        tails.update(".".join(parts[i:]) for i in range(len(parts)))
    return tails


def unused_public_functions(
    summaries: Iterable[ModuleSummary],
) -> list[tuple[str, str, int]]:
    """``(path, function, line)`` for public functions no other module uses.

    An attribute resolved to a module that is not among the files (``a.b.f``
    where ``a.b`` is a class, an object or a module re-exported under another
    name) may still reach a function, so it counts by bare name. An imported
    name does not: ``from os import f`` never reaches a function of ours.
    """
    summaries = list(summaries)
    tails = _module_tails(s.path for s in summaries)
    qualified: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
    bare: defaultdict[str, set[str]] = defaultdict(set)
    for s in summaries:
        for name in s.attributes:
            bare[name].add(s.path)
        for usage in s.imported | s.referenced:
            module, _, name = usage.rpartition(".")
            qualified[name].append((module, s.path))
            if usage in s.referenced and module not in tails:
                bare[name].add(s.path)
    star_imports = {module for s in summaries for module in s.star_imports}
    found = []
    for summary in summaries:
        path = summary.path
        if any(_matches_module(path, m) for m in star_imports):
            continue
        found.extend(
            (path, name, line)
            for name, line in summary.candidates
            if not bare[name] - {path}
            and not any(
                user != path and _matches_module(path, module)
                for module, user in qualified[name]
            )
        )
    return sorted(found, key=lambda item: (item[0], item[2]))
