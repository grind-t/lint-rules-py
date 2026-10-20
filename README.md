# lint-rules

Custom lint rules for Python projects.

```
lint-rules [root]   # default root: src; exit code 1 if there are violations
```

## Checks

| Check | What it reports |
|---|---|
| `check_public_counts` | More public top-level classes or functions per module than the package allows: classes — 1 in `_entities` and `_stateful_*`, 0 in `_stateless_*`; functions — the other way round. `Protocol` ports, enums and exceptions are not counted as classes |
| `check_single_method_classes` | Classes with a single method — use a function, `Callable` alias or `Protocol` with `__call__` |
| `check_module_names` | Modules (except `__*__.py`) whose name matches none of their public top-level names, ignoring case and `_`: `parsed_file.py` matches `ParsedFile` |
| `check_module_getattr` | Module-level `__getattr__` |
| `check_non_empty_inits` | Non-empty `__init__.py` in nested packages (re-exports) |
| `check_impure_imports` | In `_entities`, `_*_computations` and `_*_workflows`: imports of I/O-capable names from `io`, `os`, `os.path`, `pathlib`, `socket`, `subprocess` (only pure names are allowed) |
| `check_first_party_module_imports` | `import pkg.mod` or `from pkg import mod` of a first-party module — use `from pkg.mod import name` |
| `check_unimported_public_names` | Public top-level names (no `_`) that no other module imports |
