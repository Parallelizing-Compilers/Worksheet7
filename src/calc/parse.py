from lark import Lark, Tree

import calc.calc_lang as calc_lang

lark_parser = Lark("""
    %import common.CNAME
    %import common.SIGNED_INT
    %import common.SIGNED_FLOAT
    %ignore " "           // Disregard spaces in text

    literal: float_literal | int_literal
    int_literal: SIGNED_INT
    float_literal: SIGNED_FLOAT

    variable: CNAME

    // PEMDAS precedence (lowest to highest)
    expr: addsub_expr
    addsub_expr: add_expr | sub_expr
    sub_expr: (addsub_expr "-")? mul_expr
    add_expr: (addsub_expr "+")? mul_expr
    mul_expr: (mul_expr "*")? power_expr
    power_expr: primary ("^" power_expr)?
    primary: literal | variable | "(" expr ")"

    start: expr
""")


def parse(expr: str) -> calc_lang.CalcLangExpression:
    tree = lark_parser.parse(expr)
    return _parse(tree)


def _parse(tree: Tree) -> calc_lang.CalcLangExpression:
    match tree:
        case Tree(
            "start"
            | "expr"
            | "addsub_expr"
            | "primary"
            | "literal"
            | "sub_expr"
            | "power_expr"
            | "add_expr"
            | "mul_expr",
            [expr],
        ):
            return _parse(expr)
        case Tree("sub_expr", [left, right]):
            left_expr = _parse(left)
            right_expr = _parse(right)
            return calc_lang.Sub(left_expr, right_expr)
        case Tree("add_expr", [left, right]):
            left_expr = _parse(left)
            right_expr = _parse(right)
            return calc_lang.Add(left_expr, right_expr)
        case Tree("mul_expr", [left, right]):
            left_expr = _parse(left)
            right_expr = _parse(right)
            return calc_lang.Mul(left_expr, right_expr)
        case Tree("power_expr", [base, exponent]):
            base_expr = _parse(base)
            exponent_expr = _parse(exponent)
            return calc_lang.Pow(base_expr, exponent_expr)
        case Tree("primary", [expr]):
            return _parse(expr)
        case Tree("variable", [name]):
            assert isinstance(name, str)
            return calc_lang.Variable(name)
        case Tree("int_literal", [value]):
            assert isinstance(value, str)
            return calc_lang.Literal(int(value))
        case Tree("float_literal", [value]):
            assert isinstance(value, str)
            return calc_lang.Literal(float(value))
        case _:
            raise ValueError(
                f"Unexpected tree node: {tree.data} with children {tree.children}"
            )
