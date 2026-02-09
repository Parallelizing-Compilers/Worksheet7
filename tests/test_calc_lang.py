"""Tests for calc_lang nodes and interpreter."""

import pytest
from calc.calc_lang import Add, CalcLangInterpreter, Literal, Sub, Mul, Pow, Variable


class TestCalcLangInterpreter:
    """Test calc_lang interpreter execution."""

    def test_literal_evaluation(self):
        """Test evaluating a literal."""
        interp = CalcLangInterpreter()
        result = interp(Literal(10), bindings={})
        assert result == 10

    def test_simple_addition(self):
        """Test evaluating simple addition: 5 + 3."""
        interp = CalcLangInterpreter()
        expr = Add(Literal(5), Literal(3))
        result = interp(expr, bindings={})
        assert result == 8

    def test_simple_multiplication(self):
        """Test evaluating simple multiplication: 4 * 7."""
        interp = CalcLangInterpreter()
        expr = Mul(Literal(4), Literal(7))
        result = interp(expr, bindings={})
        assert result == 28

    def test_simple_power(self):
        """Test evaluating simple power: 2 ** 3."""
        interp = CalcLangInterpreter()
        expr = Pow(Literal(2), Literal(3))
        result = interp(expr, bindings={})
        assert result == 8

    def test_nested_operations(self):
        """Test evaluating nested operations: (2 + 3) * 4."""
        interp = CalcLangInterpreter()
        expr = Mul(Add(Literal(2), Literal(3)), Literal(4))
        result = interp(expr, bindings={})
        assert result == 20

    def test_complex_expression(self):
        """Test evaluating complex expression: (2 ** 3) + (4 * 5)."""
        interp = CalcLangInterpreter()
        expr = Add(Pow(Literal(2), Literal(3)), Mul(Literal(4), Literal(5)))
        result = interp(expr, bindings={})
        assert result == 28

    def test_floating_point_operations(self):
        """Test evaluating with floating point numbers: 2.5 * 4.0."""
        interp = CalcLangInterpreter()
        expr = Mul(Literal(2.5), Literal(4.0))
        result = interp(expr, bindings={})
        assert result == 10.0

    def test_power_with_floats(self):
        """Test evaluating power with floats: 2.0 ** 0.5."""
        interp = CalcLangInterpreter()
        expr = Pow(Literal(2.0), Literal(0.5))
        result = interp(expr, bindings={})
        assert abs(result - 1.414213562373095) < 1e-10


class TestCalcLangPrinter:
    """Test calc_lang string representation."""

    def test_literal_string(self):
        """Test string representation of a literal."""
        lit = Literal(42)
        assert "42" in str(lit)

    def test_add_string(self):
        """Test string representation of addition."""
        expr = Add(Literal(5), Literal(3))
        s = str(expr)
        assert "+" in s
        assert "5" in s
        assert "3" in s

    def test_mul_string(self):
        """Test string representation of multiplication."""
        expr = Mul(Literal(4), Literal(7))
        s = str(expr)
        assert "*" in s
        assert "4" in s
        assert "7" in s

    def test_pow_string(self):
        """Test string representation of power."""
        expr = Pow(Literal(2), Literal(3))
        s = str(expr)
        assert "^" in s
        assert "2" in s
        assert "3" in s

    def test_nested_string(self):
        """Test string representation of nested operations."""
        expr = Mul(Add(Literal(2), Literal(3)), Literal(4))
        s = str(expr)
        assert "*" in s
        assert "+" in s


class TestCalcLangNormalization:
    """Test normalization of calc_lang expressions."""


    @pytest.mark.parametrize(
        "program",
        [
            Add(Literal(2), Literal(3)),
            Mul(Literal(4), Literal(7)),
            Pow(Literal(2), Literal(3)),
            Add(Mul(Variable("x"), Literal(2)), Literal(3)),
            Mul(Add(Variable("x"), Literal(2)), Literal(3)),
            Mul(Sub(Variable("x"), Literal(2)), Literal(3)),
            Pow(Variable("x"), Literal(3)),
            Pow(Add(Variable("x"), Literal(2)), Literal(3)),
            Pow(Mul(Add(Variable("x"), Literal(2)), Add(Variable("x"), Literal(3))), Literal(2)),
            Sub(Mul(Add(Literal(2), Variable("x")), Add(Literal(8), Pow(Variable("x"), Literal(2)))), Sub(Literal(3), Pow(Mul(Variable("x"), Literal(4)), Literal(2)))),
        ]
    )
    def test_normalization(self, program):
        from calc.normalize import normalize, is_normalized
        program2 = normalize(program)
        assert is_normalized(program2), f"expected ... (ax^2 + (bx + c)), got {program2}"