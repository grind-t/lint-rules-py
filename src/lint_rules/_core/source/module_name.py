from lint_rules._core.shared.package_init import PACKAGE_INIT


def module_name(path: str, root: str) -> str | None:
    """Dotted name of the module the file defines under ``root``, if any.

    A package's ``__init__.py`` defines the package itself; the root's own
    ``__init__.py`` and files outside the root define no module.
    """
    prefix = "" if root.rstrip("/") in ("", ".") else root.rstrip("/") + "/"
    path = path.removeprefix("./")
    if not path.startswith(prefix) or not path.endswith(".py"):
        return None
    parts = path.removeprefix(prefix).removesuffix(".py").split("/")
    if parts[-1] == PACKAGE_INIT.removesuffix(".py"):
        parts.pop()
    return ".".join(parts) or None
