# lint-rules

Custom lint rules for Python projects.

```
lint-rules [root]   # default root: src; exit code 1 if there are violations
```

## Checks

| Check | What it reports |
|---|---|
| `check_public_classes` | More than one public top-level class per module (exceptions and enums are exempt) |
| `check_single_method_classes` | Classes with a single method — use a function, `Callable` alias or `Protocol` with `__call__` |
| `check_module_getattr` | Module-level `__getattr__` |
| `check_non_empty_inits` | Non-empty `__init__.py` in nested packages (re-exports) |
| `check_impure_imports` | Imports of I/O-capable names from `io`, `os`, `os.path`, `pathlib`, `socket`, `subprocess` (only pure names are allowed) |
| `check_plain_first_party_imports` | `import pkg.mod` of a first-party module — use `from pkg.mod import name` |
| `check_first_party_module_from_imports` | `from pkg import mod` of a first-party module — use `from pkg.mod import name` |
| `check_crowded_directories` | More than 10 modules directly in one directory |
| `check_unshared_modules` | Modules in `shared/` used by fewer than two sibling features |
| `check_unimported_public_names` | Public top-level names (no `_`) that no other module imports |
