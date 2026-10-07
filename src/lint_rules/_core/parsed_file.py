import ast
import symtable


class ParsedFile:
    """A source file with its syntax tree and symbol table, built once per file."""

    def __init__(self, path: str, source: str) -> None:
        self.path = path
        self.source = source
        self.tree = ast.parse(source)
        self.table = symtable.symtable(source, path, "exec")
