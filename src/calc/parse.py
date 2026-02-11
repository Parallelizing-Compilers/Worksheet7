from lark import Lark, Tree
import calc.calc_lang as calc_lang

# Your grammar here! Feel free to modify the below example grammar as much as
# you want, or replace it entirely.
lark_parser = Lark("""
    %import common.CNAME
    %import common.SIGNED_INT
    %import common.SIGNED_FLOAT
    %ignore " "           // Disregard spaces in text


    literal: float_literal | int_literal
    int_literal: SIGNED_INT
    float_literal: SIGNED_FLOAT

    variable: CNAME

    expr: add_expr
    add_expr: (literal "+")? literal

    start: expr
""")

def parse(expr: str) -> calc_lang.CalcLangExpression:
    tree = lark_parser.parse(expr)
    return _parse(tree)

def _parse(tree: Tree) -> calc_lang.CalcLangExpression:
    match tree:
        case Tree("start" | "literal" | "expr" | "add_expr", [expr]):
            return _parse(expr)
        case Tree("add_expr", [left, right]):
            left_expr = _parse(left)
            right_expr = _parse(right)
            return calc_lang.Add(left_expr, right_expr)
        case Tree("int_literal", [value]):
            return calc_lang.Literal(int(value))
        case Tree("float_literal", [value]):
            return calc_lang.Literal(float(value))
        case _:
            raise ValueError(
                f"Unexpected tree node: {tree.data} with children {tree.children}"
            )