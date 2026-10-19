import ast
import symtable

from lint_rules._entities.parsed_file import ParsedFile
from lint_rules._entities.source_file import SourceFile


def parse_file(file: SourceFile) -> ParsedFile:
    """Parse the source into its syntax tree and symbol table."""
    return ParsedFile(
        file.root,
        file.path,
        file.source,
        ast.parse(file.source),
        symtable.symtable(file.source, file.path, "exec"),
    )
