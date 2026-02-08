from abc import abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

from ..algebra import return_type
from ..symbolic import Context, Term, TermTree, literal_repr
from ..util import qual_str


class ExampleLangNode(Term):
    """
    ExampleLangNode

    Represents a APL2CExampleLang IR node. APL2CExampleLang is the final intermediate
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
        ctx = ExampleLangPrinterContext()
        ctx(self)
        return ctx.emit()


class ExampleLangTree(ExampleLangNode, TermTree):
    @property
    def children(self):
        """Returns the children of the node."""
        raise Exception(f"`children` isn't supported for {self.__class__}.")


class ExampleLangExpression(ExampleLangNode):
    @property
    @abstractmethod
    def result_ftype(self):
        """Returns the type of the expression."""
        ...


@dataclass(eq=True, frozen=True)
class Literal(ExampleLangExpression):
    """
    Represents the literal value `val`.

    Attributes:
        val: The literal value.
    """

    val: Any

    @property
    def result_ftype(self):
        """Returns the type of the expression."""
        return type(self.val)

    def __repr__(self) -> str:
        return literal_repr(type(self).__name__, asdict(self))


@dataclass(eq=True, frozen=True)
class Variable(ExampleLangExpression):
    """
    Represents a logical AST expression for a variable named `name`, which
    will hold a value of type `type`.

    Attributes:
        name: The name of the variable.
        type: The type of the variable.
    """

    name: str
    type: Any

    @property
    def result_ftype(self):
        """Returns the type of the expression."""
        return self.type

    def __repr__(self) -> str:
        return literal_repr(type(self).__name__, asdict(self))


@dataclass(eq=True, frozen=True)
class Call(ExampleLangExpression, ExampleLangTree):
    """
    Represents an expression for calling the function `op` on `args...`.

    Attributes:
        op: The function to call.
        args: The arguments to call on the function.
    """

    op: Literal
    args: tuple[ExampleLangNode, ...]

    @property
    def children(self):
        """Returns the children of the node."""
        return [self.op, *self.args]

    @classmethod
    def from_children(cls, op, *args):
        return cls(op, args)

    @property
    def result_ftype(self):
        """Returns the type of the expression."""
        arg_types = [arg.result_ftype for arg in self.args]
        return return_type(self.op.val, *arg_types)


class ExampleLangPrinterContext(Context):
    def __init__(self, tab="    ", indent=0):
        super().__init__()
        self.tab = tab
        self.indent = indent

    @property
    def feed(self) -> str:
        return self.tab * self.indent

    def emit(self):
        return "\n".join([*self.preamble, *self.epilogue])

    def block(self) -> "ExampleLangPrinterContext":
        blk = super().block()
        blk.indent = self.indent
        blk.tab = self.tab
        return blk

    def subblock(self):
        blk = self.block()
        blk.indent = self.indent + 1
        return blk

    def __call__(self, prgm: ExampleLangNode):
        feed = self.feed
        match prgm:
            case Literal(value):
                return qual_str(value)
            case Variable(name, _):
                return str(name)
            case Call(Literal(_) as lit, args):
                return f"{self(lit)}({', '.join(self(arg) for arg in args)})"
            case _:
                raise NotImplementedError
