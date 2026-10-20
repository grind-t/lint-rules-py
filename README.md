# lint-rules

Custom lint rules for Python projects.

```
lint-rules [root]   # default root: src; exit code 1 if there are violations
```

## Checks

| Check | What it reports |
|---|---|
| `check_public_classes` | More public top-level classes per module than the package allows: `_entities` and `_stateful_*` — 1, `_stateless_*` — 0. `Protocol` ports, enums and exceptions are not counted |
| `check_public_functions` | More public top-level functions per module than the package allows: `_entities` and `_stateful_*` — 0, `_stateless_*` — 1 |
| `check_single_method_classes` | Classes with a single method — use a function, `Callable` alias or `Protocol` with `__call__` |
| `check_module_getattr` | Module-level `__getattr__` |
| `check_non_empty_inits` | Non-empty `__init__.py` in nested packages (re-exports) |
| `check_impure_imports` | In `_entities`, `_*_computations` and `_*_workflows`: imports of I/O-capable names from `io`, `os`, `os.path`, `pathlib`, `socket`, `subprocess` (only pure names are allowed) |
| `check_first_party_module_imports` | `import pkg.mod` of a first-party module — use `from pkg.mod import name` |
| `check_first_party_module_imports_from` | `from pkg import mod` of a first-party module — use `from pkg.mod import name` |
| `check_unimported_public_names` | Public top-level names (no `_`) that no other module imports |
