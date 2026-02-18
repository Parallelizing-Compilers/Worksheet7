import pytest

from calc import macro, calc_lang

def test_macro():
    @macro
    def example(x):
        return 2 + 3 * x

    assert example == calc_lang.Add(
        calc_lang.Literal(2),
        calc_lang.Mul(
            calc_lang.Literal(3),
            calc_lang.Variable("x")
        )
    )

    @macro
    def example2(x, y):
        return (x + y) * (x - y)

    assert example2 == calc_lang.Mul(
        calc_lang.Add(
            calc_lang.Variable("x"),
            calc_lang.Variable("y")
        ),
        calc_lang.Sub(
            calc_lang.Variable("x"),
            calc_lang.Variable("y")
        )
    )

    @macro
    def example3(x):
        return (x + 1) ** 2
    assert example3 == calc_lang.Pow(
        calc_lang.Add(
            calc_lang.Variable("x"),
            calc_lang.Literal(1)
        ),
        calc_lang.Literal(2)
    )