from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..symbolic import ScopedDict, fisinstance
from . import nodes as exmpl

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
        self.bindings = bindings
        self.types = {}

    def __call__(self, prgm: exmpl.CalcLangNode):
        """
        Run the program.
        """
        match prgm:
            case exmpl.Literal(value):
                return value
            case exmpl.Variable(var_n):
                if var_n in self.bindings:
                    return self.bindings[var_n]
                raise KeyError(
                    f"Variable '{var_n}' is not defined in the current context."
                )
            case exmpl.Add(left, right):
                return self(left) + self(right)
            case exmpl.Mul(left, right):
                return self(left) * self(right)
            case exmpl.Pow(base, exponent):
                return self(base) ** self(exponent)
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
        machine = CalcLangMachine(bindings)
        return machine(prgm)