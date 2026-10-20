import ast

from lint_rules._stateless_computations.ast_statements import ast_statements


def test_yields_statements_in_source_order():
    source = """\
import a
def f():
    import b
try:
    import c
except E:
    import d
else:
    import e
finally:
    import f
match x:
    case 1:
        import g
import h
"""
    names = [
        node.names[0].name
        for node in ast_statements(ast.parse(source))
        if isinstance(node, ast.Import)
    ]
    assert names == ["a", "b", "c", "d", "e", "f", "g", "h"]
