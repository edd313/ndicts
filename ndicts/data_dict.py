from abc import ABC, abstractmethod
from functools import reduce
from numbers import Number
from typing import Any, Callable

from ndicts import NestedDict


class _Arithmetics(ABC):
    """
    Mixin class providing methods for arithmetic operations.
    Useful when all operations share the same base mechanism.
    """

    @abstractmethod
    def _arithmetic_operation(
        self, other, operation: str = "__add__", symbol: str = "+"
    ):
        """General implementation of any arithmetic operation, just pass the operation and symbol
        Once this is defined all methods below should work"""
        raise NotImplementedError

    def __add__(self, other):
        return self._arithmetic_operation(other, "__add__", "+")

    def __sub__(self, other):
        return self._arithmetic_operation(other, "__sub__", "-")

    def __mul__(self, other):
        return self._arithmetic_operation(other, "__mul__", "*")

    def __truediv__(self, other):
        return self._arithmetic_operation(other, "__truediv__", "/")

    def __floordiv__(self, other):
        return self._arithmetic_operation(other, "__floordiv__", "//")

    def __mod__(self, other):
        return self._arithmetic_operation(other, "__mod__", "%")

    def __pow__(self, other):
        return self._arithmetic_operation(other, "__pow__", "**")

    def __neg__(self):
        return self * -1


class DataDict(NestedDict, _Arithmetics):
    """A NestedDict that supports arithmetics.
    Other methods are included that make DataDict similar to DataFrames."""

    def _arithmetic_operation(self, other, operation: str, symbol: str):
        """Implements any arithmetic operation, just pass the underlying method as string
        The symbol, passed as a string, will appear in the exception message if any
        The operation is performed only between NestedProperties or with numbers"""
        result = self.copy()
        if isinstance(other, self.__class__):
            for other_key, other_value in other.items():
                if other_key in self:
                    for key, value in self.extract[other_key].items():
                        result[key] = getattr(value, operation).__call__(other_value)
                else:
                    raise TypeError(
                        f"unsupported operand type(s) for {symbol}: incompatible keys"
                    )
            return result

        elif isinstance(other, Number):
            for key, value in self.items():
                result[key] = getattr(value, operation).__call__(other)
            return result

        return TypeError(
            f"unsupported operand type(s) for {symbol}: {type(self)} and {type(other)}"
        )

    def apply(self, func: Callable, inplace: bool = False):
        """Apply func to all values."""
        if inplace:
            for key, leaf in self.items():
                self[key] = func(leaf)
        else:
            new_self = self.copy()
            for key, leaf in new_self.items():
                new_self[key] = func(leaf)
            return new_self

    def reduce(self, func: Callable, *initial: Any):
        """Pass func and initial to functools.reduce and apply it to all values."""
        return reduce(func, self.values(), *initial)

    def total(self):
        """Returns sum of all values."""
        return sum(self.values())

    def mean(self) -> Number:
        """Returns mean of all values."""
        return self.total() / len(self)

    def std(self) -> Number:
        """Returns standard deviation of all values."""
        step = self.reduce(lambda a, b: a + (b - self.mean()) ** 2, 0)
        step /= len(self) - 1
        return step**0.5