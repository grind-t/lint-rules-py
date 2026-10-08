import ast
import symtable

from lint_rules._core.source_file import SourceFile


class ParsedFile:
    """A source file with its syntax tree and symbol table, built once per file."""

    def __init__(self, file: SourceFile) -> None:
        self.root = file.root
        self.path = file.path
        self.source = file.source
        self.tree = ast.parse(file.source)
        self.table = symtable.symtable(file.source, file.path, "exec")
