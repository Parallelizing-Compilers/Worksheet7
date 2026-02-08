from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..symbolic import ScopedDict, fisinstance
from . import nodes as exmpl


@dataclass(eq=True)
class HaltState:
    """
    A class to represent the halt state of an assembly program.
    This is used to indicate whether we should break or return, and
    what the return value is if applicable.
    """
    should_halt: bool = False
    return_value: Any = None


class CalcLangMachine:
    """
    An interpreter for CALCCalcLang.
    """

    def __init__(
        self,
        bindings=None,
    ):
        if bindings is None:
            bindings = ScopedDict()

    def __call__(self, prgm: exmpl.CalcLangNode):
        """
        Run the program.
        """
        match prgm:
            case exmpl.Literal(value):
                return value
            case exmpl.Variable(var_n, var_t):
                if var_n in self.types:
                    def_t = self.types[var_n]
                    if def_t != var_t:
                        raise TypeError(
                            f"Variable '{var_n}' is declared as type {def_t}, "
                            f"but used as type {var_t}."
                        )
                if var_n in self.bindings:
                    return self.bindings[var_n]
                raise KeyError(
                    f"Variable '{var_n}' is not defined in the current context."
                )
            case exmpl.Call(f, args):
                f_e = self(f)
                args_e = [self(arg) for arg in args]
                return f_e(*args_e)
            case _:
                raise NotImplementedError(
                    f"Unrecognized assembly node type: {type(prgm)}"
                )

class CalcLangInterpreter:
    """
    A class to represent an interpreter for CALCCalcLang.
    This is a simple wrapper around the CalcLangMachine that provides
    a more user-friendly interface for running programs.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose

    def __call__(self, prgm: exmpl.CalcLangNode, bindings=None):
        return self.machine(bindings)(prgm)