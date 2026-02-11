# CALC

CALC is a simple calculator language.

in `src/calc/calc_lang/nodes.py`, we have defined the following nodes:
- `Literal`: Represents a literal value (e.g., a number).
- `Variable`: Represents a variable (e.g., 'x').
- `Add`: Represents the addition of two expressions.
- `Sub`: Represents the subtraction of two expressions.
- `Mul`: Represents the multiplication of two expressions.
- `Pow`: Represents the exponentiation of a base expression to an exponent expression.

The `CalcLangInterpreter` class in `src/calc/calc_lang/interpreter.py` provides a method to evaluate these nodes.

## Installation

CALC uses [poetry](https://python-poetry.org/) for packaging. To install for development, clone the repository and run one of the following

1. `[Option 1]`: personal machine
```bash
poetry install --extras test
```


2. `[Option 2]`: PACE
```bash
student@local:~> ssh <gatech_username>@login-ice.pace.gatech.edu
student@login-ice-1:~> cd scratch
student@login-ice-1:~> git clone https://github.com/Parallelizing-Compilers/CALC.git
student@login-ice-1:~> cd CALC
student@login-ice-1:~> salloc -N 1 -ntasks-per-node 1 -t 60 -C gold6226
student@atl1-1-02-003-19-2:~> module load python/3.12.5
student@atl1-1-02-003-19-2:~> python3 -m venv calc
student@atl1-1-02-003-19-2:~> source wk7/bin/activate
student@atl1-1-02-003-19-2:~> pip install -r requirements.txt
student@atl1-1-02-003-19-2:~> pip install .
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, development setup, and best practices.

### Worksheet 7: Normalization

 In this worksheet, you'll implement a normalization pass that rewrites Calc expressions into the standard form for polynomials:

$a_{n}x^{n}+a_{n-1}x^{n-1}+\dotsb +a_{2}x^{2}+a_{1}x+a_{0}$

where $a_{n}$ are coefficients and $x$ is the variable.

Your task is to implement the normalization logic in `src/calc/normalize.py` so that it can take any expression composed of these nodes and rewrite it into the standard polynomial form.

You can run the simple test cases provided in `tests/test_calc_lang.py` to verify your implementation. The tests check if the normalization process correctly transforms various expressions into their normalized polynomial form.

Run tests with:
1. `[Option 1]`: personal machine
```bash
poetry run pytest tests/test_normalize.py
```

2. `[Option 2]`: PACE
```bash
pytest tests/test_normalize.py
```

### Worksheet 8: Parsing

In this worksheet, you'll implement a parser that takes a string representation of a CALC expression and converts it into the corresponding AST using the nodes defined in `src/calc/calc_lang/nodes.py`.

Fill out the grammar and parsing logic in `src/calc/parser.py` to achieve this. The parser should be able to handle expressions that include literals, variables, addition, subtraction, multiplication, and exponentiation, and follow operator precedence rules like PEMDAS.

You may find the [lark documentation](https://lark-parser.readthedocs.io/en/stable/) helpful for implementing the parser.

Run tests with:
1. `[Option 1]`: personal machine
```bash
poetry run pytest tests/test_parse.py
```

2. `[Option 2]`: PACE
```bash
pytest tests/test_parse.py
```

