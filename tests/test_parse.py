import pytest

from calc.calc_lang import Add, Literal, Mul, Pow, Sub, Variable


class TestCalcLangParser:
    """Test parsing of calc_lang expressions."""

    @pytest.mark.parametrize(
        "program_str, expected_ast",
        [
            ("42", Literal(42)),
            ("x", Variable("x")),
            ("2 + 3", Add(Literal(2), Literal(3))),
            ("4 * 7", Mul(Literal(4), Literal(7))),
            ("2 ^ 3", Pow(Literal(2), Literal(3))),
            ("(2 + 3) * 4", Mul(Add(Literal(2), Literal(3)), Literal(4))),
            (
                "(2 ^ 3) + (4 * 5)",
                Add(Pow(Literal(2), Literal(3)), Mul(Literal(4), Literal(5))),
            ),
            ("2.5 * 4.0", Mul(Literal(2.5), Literal(4.0))),
            ("2.0 ^ 0.5", Pow(Literal(2.0), Literal(0.5))),
            ("2 + x * 4", Add(Literal(2), Mul(Variable("x"), Literal(4)))),
            ("2 * 3 + 4", Add(Mul(Literal(2), Literal(3)), Literal(4))),
            ("y ^ 3 * 4", Mul(Pow(Variable("y"), Literal(3)), Literal(4))),
            ("2 * 3 ^ 4", Mul(Literal(2), Pow(Literal(3), Literal(4)))),
            ("a + 3 - 4", Sub(Add(Variable("a"), Literal(3)), Literal(4))),
            ("2 * 3 * 4", Mul(Mul(Literal(2), Literal(3)), Literal(4))),
            ("2 ^ z + 4", Add(Pow(Literal(2), Variable("z")), Literal(4))),
            ("2 - 3 * 4", Sub(Literal(2), Mul(Literal(3), Literal(4)))),
            ("2 * b - 4", Sub(Mul(Literal(2), Variable("b")), Literal(4))),
            ("2 ^ 3 ^ 4", Pow(Literal(2), Pow(Literal(3), Literal(4)))),
            (
                "(x + 3) * (4 - 5)",
                Mul(Add(Variable("x"), Literal(3)), Sub(Literal(4), Literal(5))),
            ),
            (
                "(2 ^ 3) ^ (4 + 1)",
                Pow(Pow(Literal(2), Literal(3)), Add(Literal(4), Literal(1))),
            ),
            (
                "2 + 3 - 4 - 5",
                Sub(Sub(Add(Literal(2), Literal(3)), Literal(4)), Literal(5)),
            ),
            (
                "y * 3 + 4 * 5",
                Add(Mul(Variable("y"), Literal(3)), Mul(Literal(4), Literal(5))),
            ),
            (
                "1 + 2 * 3 ^ 4 - 5",
                Sub(
                    Add(Literal(1), Mul(Literal(2), Pow(Literal(3), Literal(4)))),
                    Literal(5),
                ),
            ),
            (
                "(1 + 2) * (3 + 4) + 5",
                Add(
                    Mul(Add(Literal(1), Literal(2)), Add(Literal(3), Literal(4))),
                    Literal(5),
                ),
            ),
            (
                "2 ^ (3 + n) * (5 - 1)",
                Mul(
                    Pow(Literal(2), Add(Literal(3), Variable("n"))),
                    Sub(Literal(5), Literal(1)),
                ),
            ),
        ],
    )
    def test_parsing(self, program_str, expected_ast):
        from calc.parse import parse

        ast = parse(program_str)
        assert ast == expected_ast, (
            f"parsing {program_str} produced {ast}, expected {expected_ast}"
        )
