from .calc_lang import Add, CalcLangExpression, Literal, Mul, Pow, Variable
from .symbolic import Fixpoint, PostWalk, Rewrite


def normalize(node: CalcLangExpression):
    def rewrite(node: CalcLangExpression):
        match node:
            case Add(Literal(x), Literal(y)):
                return Literal(x + y)
            case Mul(Add(a, b), c):
                return Add(Mul(a, c), Mul(b, c))
            case Mul(x, Pow(y, Literal(n))) if x == y:
                return Pow(x, Literal(n + 1))
            # Your normalization rules here!
            # Feel free to delete the above examples if you want.
            case _:
                return None

    return Rewrite(Fixpoint(PostWalk(rewrite)))(node)


def _is_normalized(node: CalcLangExpression):
    match node:
        case Add(Mul(Literal(_), Pow(Variable(x), Literal(n))), y):
            z, m, c = _is_normalized(y)
            if c and x == z and n == m + 1:
                return x, n, c
            return (None, None, False)
        case Add(Mul(Literal(_), Variable(x)), Literal(c)):
            return x, 1, True
        case Literal(_):
            return (None, 0, True)
        case _:
            return (None, None, False)


def is_normalized(node: CalcLangExpression):
    """
    check if the expression is in normalized form, i.e. it is of the form
        ... ((a * x^2) + ((b * x) + c))

    where a, b, c are constants and x is a variable. Note the nesting of parens.
    """
    return _is_normalized(node)[2]
