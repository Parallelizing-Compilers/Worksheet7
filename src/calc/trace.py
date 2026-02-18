from calc import calc_lang


class Tracer:
    """A tracer to construct a calc_lang expression from a Python expression."""

    expr: calc_lang.CalcLangExpression

    def __init__(self, expr: calc_lang.CalcLangExpression):
        self.expr = expr

    def __add__(self, other):
        return Tracer(calc_lang.Add(self.expr, trace(other).expr))

    # Your implementation here!
    # https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types


def trace(name) -> Tracer:
    if isinstance(name, Tracer):
        return name
    if isinstance(name, str):
        return Tracer(calc_lang.Variable(name))
    if isinstance(name, int | float):
        return trace_lit(name)
    raise ValueError(f"Expected a string or a number, got {name} of type{type(name)}")


def trace_lit(value: float) -> Tracer:
    return Tracer(calc_lang.Literal(value))
