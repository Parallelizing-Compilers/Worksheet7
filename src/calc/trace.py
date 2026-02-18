from calc import calc_lang


class Tracer:
    """A tracer to construct a calc_lang expression from a Python expression."""

    expr: calc_lang.CalcLangExpression

    def __init__(self, expr: calc_lang.CalcLangExpression):
        self.expr = expr

    def __add__(self, other):
        return Tracer(calc_lang.Add(self.expr, trace(other).expr))
    
    def __radd__(self, other):
        return Tracer(calc_lang.Add(trace(other).expr, self.expr))
    
    def __sub__(self, other):
        return Tracer(calc_lang.Sub(self.expr, trace(other).expr))
    
    def __rsub__(self, other):
        return Tracer(calc_lang.Sub(trace(other).expr, self.expr))
    
    def __mul__(self, other):
        return Tracer(calc_lang.Mul(self.expr, trace(other).expr))
    
    def __rmul__(self, other):
        return Tracer(calc_lang.Mul(trace(other).expr, self.expr))
    
    def __pow__(self, other):
        return Tracer(calc_lang.Pow(self.expr, trace(other).expr))
    
    def __rpow__(self, other):
        return Tracer(calc_lang.Pow(trace(other).expr, self.expr))

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
