import ast
import symtable
from dataclasses import asdict

from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.source_file import SourceFile


def parse_file(file: SourceFile) -> ParsedFile:
    """Parse the source into its syntax tree and symbol table."""
    return ParsedFile(
        **asdict(file),
        tree=ast.parse(file.source),
        table=symtable.symtable(file.source, file.path, "exec"),
    )
