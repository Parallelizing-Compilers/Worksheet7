import dill
import ast
from textwrap import dedent
from . import calc_lang

def macro(f):
    #inspect.getsource is a base python dep, but doesn't always work in REPL
    source = dill.source.getsource(f)
    #if the function is a closure, the source might be indented
    source = dedent(source)
    #print(source)
    tree = ast.parse(source)
    #print(ast.dump(tree, indent=2))
    match tree:
        case ast.Module(body=[
            ast.FunctionDef(name=_, args=_, body=[
                ast.Return(value=node)
            ], decorator_list=_)
        ]):
            return _parse(node)
        case _:
            raise ValueError("Expected a function with a single expression in the body")



def _parse(node):
    match node:
        case ast.Constant(value):
            return calc_lang.Literal(value)
        #your parsing rules here! Check the ast module docs for hints.
        case _:
            raise ValueError(f"Unsupported AST node: {node}")
