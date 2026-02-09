# Worksheet 7: Rewriting CALC

A python compiler that translates CALC code to C code.

## Installation

CALC uses [poetry](https://python-poetry.org/) for packaging. To install for development, clone the repository and run one of the following

1. `[Option 1]`: personal machine
```bash
poetry install --extras test
```


2. `[Option 2]`: PACE
```bash
module load python/3.12.5
python3 -m venv wk7
source wk7/bin/activate
pip install -r requirements.txt
pip install .
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, development setup, and best practices.


### Overview

CALC is a simple calculator language. In this worksheet, you'll implement a normalization pass that rewrites Calc expressions into the standard form for polynomials:

$a_{n}x^{n}+a_{n-1}x^{n-1}+\dotsb +a_{2}x^{2}+a_{1}x+a_{0}$

where $a_{n}$ are coefficients and $x$ is the variable. 

in `src/calc/calc_lang/nodes.py`, we have defined the following nodes:
- `Literal`: Represents a literal value (e.g., a number).
- `Variable`: Represents a variable (e.g., 'x').
- `Add`: Represents the addition of two expressions.
- `Sub`: Represents the subtraction of two expressions.
- `Mul`: Represents the multiplication of two expressions.
- `Pow`: Represents the exponentiation of a base expression to an exponent expression.

The `CalcLangInterpreter` class in `src/calc/calc_lang/interpreter.py` provides a method to evaluate these nodes.

Your task is to implement the normalization logic in `src/calc/normalize.py` so that it can take any expression composed of these nodes and rewrite it into the standard polynomial form.

You can run the simple test cases provided in `tests/test_calc_lang.py` to verify your implementation. The tests check if the normalization process correctly transforms various expressions into their normalized polynomial form.

Run tests with:
1. `[Option 1]`: personal machine
```bash
poetry run pytest
```

2. `[Option 2]`: PACE
```bash
pytest tests/
```