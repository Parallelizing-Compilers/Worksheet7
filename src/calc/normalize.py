from .calc_lang import CalcLangExpression, Literal, Variable, Add, Mul, Pow
from .symbolic import Rewrite, Fixpoint, PostWalk 

def normalize(node:CalcLangExpression):
    def rewrite(node:CalcLangExpression):
        match node:
            case Add(Literal(x), Literal(y)):
                return Literal(x + y)
            case Mul(Add(a, b), c):
                return Add(Mul(a, c), Mul(b, c))
            case Mul(x, Pow(y, Literal(n))) if x == y:
                return Pow(x, Literal(n + 1))
            case _:
                return None
    return Rewrite(Fixpoint(PostWalk(rewrite)))(node)

def _is_normalized(node:CalcLangExpression):
    match node:
        case Add(Mul(Literal(a), Pow(Variable(x), Literal(n))), y):
            z, m, c = _is_normalized(y)
            if c and x == z and n == m + 1:
                return x, n, c
            else:
                return (None, None, False)
        case Add(Mul(Literal(a), Variable(x)), Literal(c)):
            return x, 1, True
        case Literal(_):
            return (None, 0, True)
        case _:
            return (None, None, False)

def is_normalized(node:CalcLangExpression):
    """
    check if the expression is in normalized form, i.e. it is of the form
        ... (ax^2 + (bx + c))
    """
    return _is_normalized(node)[2]

            

