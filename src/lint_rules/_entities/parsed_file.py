import ast
import symtable
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedFile:
    """A source file with its syntax tree and symbol table, built once per file."""

    root: str
    path: str
    source: str
    tree: ast.Module
    table: symtable.SymbolTable
