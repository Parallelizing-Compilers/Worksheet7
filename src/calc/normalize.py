from .calc_lang import Add, CalcLangExpression, Literal, Mul, Pow, Variable, Sub
from .symbolic import Fixpoint, PostWalk, Rewrite, Chain


def normalize(node: CalcLangExpression):
    #first, apply distributive property and reassociate
    def rewrite0(node: CalcLangExpression):
        match node:
            case Sub(x, y):
                return Add(x, Mul(Literal(-1), y))
            case Add(Literal(x), Literal(y)):
                return Literal(x + y)
            case Mul(Literal(x), Literal(y)):
                return Literal(x * y)
            case Pow(Literal(x), Literal(y)):
                return Literal(x ** y)
            case Mul(Add(a, b), c):
                return Add(Mul(a, c), Mul(b, c))
            case Mul(a, Add(b, c)):
                return Add(Mul(a, b), Mul(a, c))
            case Pow(x, Literal(0)):
                return Literal(1)
            case Pow(x, Literal(1)):
                return x
            case Pow(x, Literal(y)):
                return Mul(x, Pow(x, Literal(y - 1)))
            case Add(Add(x, y), z):
                return Add(x, Add(y, z))
            case Mul(Mul(x, y), z):
                return Mul(x, Mul(y, z))
            case Pow(Pow(x, y), z):
                return Pow(x, Mul(y, z))
            case _:
                return None
    
    #replace variables with x^1, so that we can combine them with the same base later
    def rewrite1(node: CalcLangExpression):
        match node:
            case Variable(x):
                return Pow(Variable(x), Literal(1))
            case _:
                return None
    
    #combine like terms, e.g. x^2 * x^3 -> x^5, 2 * 3 -> 6, 2 * (3 * x) -> 6 * x, etc.
    def rewrite2(node: CalcLangExpression):
        match node:
            case Mul(Pow(x, Literal(n)), Pow(y, Literal(m))) if x == y:
                return Pow(x, Literal(n + m))
            case Mul(Pow(x, Literal(n)), Mul(Pow(y, Literal(m)), z)) if x == y:
                return Mul(Pow(x, Literal(n + m)), z)
            case Mul(Literal(x), Literal(y)):
                return Literal(x * y)
            case Mul(Literal(x), Mul(Literal(y), z)):
                return Mul(Literal(x * y), z)
            case Mul(Pow(y, n), Mul(Literal(x), z)):
                return Mul(Literal(x), Mul(Pow(y, n), z))
            case Mul(Pow(y, n), Literal(x)):
                return Mul(Literal(x), Pow(y, n))
            case _:
                return None
    
    #sort the expression for the is_normalized check, i.e. ... ((a * x^2) + ((b * x) + c))
    def rewrite3(node: CalcLangExpression):
        match node:
            case Add(Literal(a), Literal(b)):
                return Literal(a + b)
            case Add(Literal(a), Add(Literal(b), c)):
                return Add(Literal(a + b), c)
            case Add(Literal(a), Add(b, c)):
                return Add(b, Add(Literal(a), c))
            case Add(Literal(a), Mul(Literal(b), Pow(x, Literal(n)))):
                return Add(Mul(Literal(b), Pow(x, Literal(n))), Literal(a))
            case Add(Pow(x, Literal(n)), y):
                return Add(Mul(Literal(1), Pow(x, Literal(n))), y)
            case Add(Mul(a, Pow(x, Literal(n))), Add(Mul(b, Pow(y, Literal(m))), z)) if n < m:
                return Add(Mul(b, Pow(y, Literal(m))), Add(Mul(a, Pow(x, Literal(n))), z))
            case Add(Mul(Literal(a), Pow(x, Literal(n))), Add(Mul(Literal(b), Pow(y, Literal(m))), z)) if n == m:
                return Add(Mul(Literal(a + b), Pow(x, Literal(n))), z)
            case _:
                return None

    #fill missing terms
    def rewrite4(node: CalcLangExpression):
        match node:
            case Add(Mul(a, Pow(x, Literal(n))), Add(Mul(b, Pow(y, Literal(m))), z)) if n > m + 1:
                return Add(Mul(a, Pow(x, Literal(n))), Add(Mul(Literal(0), Pow(x, Literal(m + 1))), Add(Mul(b, Pow(y, Literal(m))), z)))
            case Add(Mul(a, Pow(x, Literal(n))), Literal(b)) if n > 1:
                return Add(Mul(a, Pow(x, Literal(n))), Add(Mul(Literal(0), Pow(x, Literal(1))), Literal(b)))
            case _:
                return None

    #simplify
    def rewrite5(node: CalcLangExpression):
        match node:
            case Pow(x, Literal(1)):
                return x
            case _:
                return None
    
    node = Add(node, Literal(0))
    node = Rewrite(Chain((
        Fixpoint(PostWalk(rewrite0)),
        PostWalk(rewrite1),
        Fixpoint(PostWalk(rewrite2)),
        Fixpoint(PostWalk(rewrite3)),
        Fixpoint(PostWalk(rewrite4)),
        Fixpoint(PostWalk(rewrite5))
    )))(node)
    return node


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
