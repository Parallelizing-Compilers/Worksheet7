import pytest

from calc import trace, calc_lang

def test_trace_add():
    result = trace("x") + 2
    assert result.expr == calc_lang.Add(
        calc_lang.Variable("x"),
        calc_lang.Literal(2)
    )

def test_trace_pythagorean():
    a = trace("a")
    b = trace("b")
    result = ((a * a) + (b * b)) ** 0.5
    assert result.expr == calc_lang.Power(
        calc_lang.Add(
            calc_lang.Mul(
                calc_lang.Variable("a"),
                calc_lang.Variable("a")
            ),
            calc_lang.Mul(
                calc_lang.Variable("b"),
                calc_lang.Variable("b")
            )
        ),
        calc_lang.Literal(0.5)
    )

def test_trace_sub():
    result = 3 - trace("x")
    assert result.expr == calc_lang.Sub(
        calc_lang.Literal(3),
        calc_lang.Variable("x")
    )

def test_trace_pow():
    def pow(x, n):
        if n == 0:
            return 1
        else:
            return x * pow(x, n - 1)

    result = trace(pow(trace("x"), 5))
    assert result.expr == calc_lang.Mul(
        calc_lang.Variable("x"),
        calc_lang.Mul(
            calc_lang.Variable("x"),
            calc_lang.Mul(
                calc_lang.Variable("x"),
                calc_lang.Mul(
                    calc_lang.Variable("x"),
                    calc_lang.Mul(
                        calc_lang.Variable("x"),
                        calc_lang.Literal(1)
                    )
                )
            )
        )
    )