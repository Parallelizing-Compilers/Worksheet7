from calc import calc_lang

class Tracer:
    """A tracer to construct a calc_lang expression from a Python expression."""
    expr: calc_lang.CalcLangExpression

    def __init__(self, expr: calc_lang.CalcLangExpression):
        self.expr = expr

    def __add__(self, other):
        return Tracer(calc_lang.Add(self.expr, trace(other).expr))

    # Your implementation here!
    #https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types

def trace(name) -> Tracer:
    if isinstance(name, Tracer):
        return name
    elif isinstance(name, str):
        return Tracer(calc_lang.Variable(name))
    elif isinstance(name, int) or isinstance(name, float):
        return trace_lit(name)
    else:
        raise ValueError(f"Expected a string or a number, got {name} of type"
            f"{type(name)}")

def trace_lit(value: int | float) -> Tracer:
    return Tracer(calc_lang.Literal(value))