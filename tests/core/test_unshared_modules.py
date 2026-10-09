from lint_rules._core.layout.unshared_modules import unshared_modules

_MODULES = {
    "lib.shared": "lib/shared/__init__.py",
    "lib.shared.base": "lib/shared/base.py",
    "lib.shared.walk": "lib/shared/walk.py",
}


def _check(imports: dict[str, set[str]]):
    files: dict[str, set[str]] = {path: set() for path in _MODULES.values()}
    return unshared_modules(files | imports, _MODULES)


def test_unshared_modules(subtests):
    cases = {
        "module used by two features is shared": (
            {"lib/a/x.py": {"lib.shared.base"}, "lib/b/y.py": {"lib.shared.base"}},
            [("lib/shared/walk.py", ())],
        ),
        "module used by one feature is reported": (
            {"lib/a/x.py": {"lib.shared.base"}, "lib/a/y.py": {"lib.shared.base"}},
            [("lib/shared/base.py", ("a",)), ("lib/shared/walk.py", ())],
        ),
        "used through another shared module": (
            {
                "lib/shared/walk.py": {"lib.shared.base"},
                "lib/a/x.py": {"lib.shared.walk"},
                "lib/b/y.py": {"lib.shared.walk"},
            },
            [],
        ),
        "importers outside the owner and directly in it are not features": (
            {
                "app/x.py": {"lib.shared.base", "lib.shared.walk"},
                "lib/main.py": {"lib.shared.base", "lib.shared.walk"},
                "lib/a/x.py": {"lib.shared.base", "lib.shared.walk"},
            },
            [("lib/shared/base.py", ("a",)), ("lib/shared/walk.py", ("a",))],
        ),
    }
    for name, (imports, expected) in cases.items():
        with subtests.test(name):
            assert _check(imports) == expected


def test_nearest_shared_owns_the_module():
    modules = {"lib.a.shared.base": "lib/a/shared/base.py"}
    imports = {
        "lib/a/shared/base.py": set(),
        "lib/a/p/x.py": {"lib.a.shared.base"},
        "lib/a/q/y.py": {"lib.a.shared.base"},
    }
    assert unshared_modules(imports, modules) == []


def test_ignores_modules_outside_shared():
    modules = {"lib.a.x": "lib/a/x.py"}
    assert unshared_modules({"lib/a/x.py": set()}, modules) == []
