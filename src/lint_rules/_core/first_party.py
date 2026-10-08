from collections.abc import Container


def is_first_party(module: str, top_level_modules: Container[str]) -> bool:
    """Whether ``module`` belongs to one of the project's top-level modules."""
    return module.partition(".")[0] in top_level_modules
