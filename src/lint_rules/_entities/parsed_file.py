import ast
import symtable
from dataclasses import dataclass

from lint_rules._entities.source_file import SourceFile


@dataclass(frozen=True, kw_only=True)
class ParsedFile(SourceFile):
    """A source file with its syntax tree and symbol table, built once per file."""

    tree: ast.Module
    table: symtable.SymbolTable
