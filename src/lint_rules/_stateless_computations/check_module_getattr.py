import symtable

from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.violation import Violation
from lint_rules._entities.violation_module_getattr import ViolationModuleGetattr

_NAME = "__getattr__"


def _binds_module_getattr(table: symtable.SymbolTable) -> bool:
    """Whether the module binds ``__getattr__`` at module level.

    The symbol table covers every binding form (def, assignment, import,
    for, with, match, ...); methods and nested functions live in child
    tables and are ignored.
    """
    if _NAME not in table.get_identifiers():
        return False
    symbol = table.lookup(_NAME)
    return symbol.is_assigned() or symbol.is_imported()


def check_module_getattr(file: ParsedFile) -> list[Violation]:
    if not _binds_module_getattr(file.table):
        return []
    return [ViolationModuleGetattr(file.path)]
