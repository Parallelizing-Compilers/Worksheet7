from abc import abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

from ..symbolic import Context, Term, TermTree, literal_repr
from ..util import qual_str


class CalcLangNode(Term):
    """
    CalcLangNode

    Represents a CALCCalcLang IR node. CALCCalcLang is the final intermediate
    representation before code generation (translation to the output language).
    It is a low-level imperative description of the program, with control flow,
    linear memory regions called "buffers", and explicit memory management.
    """

    @classmethod
    def head(cls):
        """Returns the head of the node."""
        return cls

    @classmethod
    def make_term(cls, head, *args):
        """Creates a term with the given head and arguments."""
        return head.from_children(*args)

    @classmethod
    def from_children(cls, *children):
        """
        Creates a term from the given children. This is used to create terms
        from the children of a node.
        """
        return cls(*children)

    def __str__(self):
        """Returns a string representation of the node."""
        ctx = CalcLangPrinterContext()
        return ctx(self) or ""


class CalcLangTree(CalcLangNode, TermTree):
    @property
    def children(self):
        """Returns the children of the node."""
        raise Exception(f"`children` isn't supported for {self.__class__}.")


class CalcLangExpression(CalcLangNode):
    ...


@dataclass(eq=True, frozen=True)
class Literal(CalcLangExpression):
    """
    Represents the literal value `val`.

    Attributes:
        val: The literal value.
    """

    val: Any

    def __repr__(self) -> str:
        return literal_repr(type(self).__name__, asdict(self))


@dataclass(eq=True, frozen=True)
class Variable(CalcLangExpression):
    """
    Represents a logical AST expression for a variable named `name`, which
    will hold a value of type `type`.

    Attributes:
        name: The name of the variable.
    """

    name: str

    def __repr__(self) -> str:
        return literal_repr(type(self).__name__, asdict(self))


@dataclass(eq=True, frozen=True)
class Add(CalcLangExpression, CalcLangTree):
    """
    Represents an addition expression: left + right.

    Attributes:
        left: The left operand.
        right: The right operand.
    """

    left: CalcLangExpression
    right: CalcLangExpression

    @property
    def children(self):
        """Returns the children of the node."""
        return [self.left, self.right]

@dataclass(eq=True, frozen=True)
class Sub(CalcLangExpression, CalcLangTree):
    """
    Represents a subtraction expression: left - right.

    Attributes:
        left: The left operand.
        right: The right operand.
    """

    left: CalcLangExpression
    right: CalcLangExpression

    @property
    def children(self):
        """Returns the children of the node."""
        return [self.left, self.right]


@dataclass(eq=True, frozen=True)
class Mul(CalcLangExpression, CalcLangTree):
    """
    Represents a multiplication expression: left * right.

    Attributes:
        left: The left operand.
        right: The right operand.
    """

    left: CalcLangExpression
    right: CalcLangExpression

    @property
    def children(self):
        """Returns the children of the node."""
        return [self.left, self.right]


@dataclass(eq=True, frozen=True)
class Pow(CalcLangExpression, CalcLangTree):
    """
    Represents a power expression: base ** exponent.

    Attributes:
        base: The base operand.
        exponent: The exponent operand.
    """

    base: CalcLangExpression
    exponent: CalcLangExpression

    @property
    def children(self):
        """Returns the children of the node."""
        return [self.base, self.exponent]


class CalcLangPrinterContext(Context):
    def __init__(self, tab="    ", indent=0):
        super().__init__()
        self.tab = tab
        self.indent = indent

    @property
    def feed(self) -> str:
        return self.tab * self.indent

    def emit(self):
        return "\n".join([*self.preamble, *self.epilogue])

    def block(self) -> "CalcLangPrinterContext":
        blk = super().block()
        blk.indent = self.indent
        blk.tab = self.tab
        return blk

    def subblock(self):
        blk = self.block()
        blk.indent = self.indent + 1
        return blk

    def __call__(self, prgm: CalcLangNode):
        match prgm:
            case Literal(value):
                return qual_str(value)
            case Variable(name):
                return str(name)
            case Add(left, right):
                return f"({self(left)} + {self(right)})"
            case Sub(left, right):
                return f"({self(left)} - {self(right)})"
            case Mul(left, right):
                return f"({self(left)} * {self(right)})"
            case Pow(base, exponent):
                return f"({self(base)} ^ {self(exponent)})"
            case _:
                raise NotImplementedError
