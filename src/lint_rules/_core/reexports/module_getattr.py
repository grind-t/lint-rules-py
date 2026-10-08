import symtable

_NAME = "__getattr__"


def binds_module_getattr(table: symtable.SymbolTable) -> bool:
    """Whether the module binds ``__getattr__`` at module level.

    The symbol table covers every binding form (def, assignment, import,
    for, with, match, ...); methods and nested functions live in child
    tables and are ignored.
    """
    if _NAME not in table.get_identifiers():
        return False
    symbol = table.lookup(_NAME)
    return symbol.is_assigned() or symbol.is_imported()
