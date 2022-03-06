from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from copy import deepcopy
from itertools import product
from functools import reduce
from numbers import Number
from typing import Any, Callable, Iterable


class NestedDict(MutableMapping):
    """Class to represent data organised in nested dictionary"""

    @classmethod
    def from_product(cls, *args: Iterable, value: Any = None):
        """Initialize class by cartesian product of the arguments"""
        instance = cls()
        for key in product(*args):
            instance[key] = value
        return instance

    @classmethod
    def from_tuples(cls, *args: Iterable, value: Any = None):
        """Initialize class by providing the keys and a common value"""
        ndict = cls()
        for arg in args:
            ndict[arg] = value
        return ndict

    def __init__(self, dictionary: dict = None, copy: bool = False):
        """Initialize a NestedDict from a dictionary.
        Set copy to True to use a copy of the input dictionary"""
        if dictionary is None:
            dictionary = {}
        self._ndict = deepcopy(dictionary) if copy else dictionary

    def __getitem__(self, key):
        if not isinstance(key, tuple):
            key = (key,)
        item = self._ndict

        for k in key:
            try:
                item = item[k]
            except KeyError:
                raise KeyError(key)
            except TypeError:
                raise KeyError(key)
        return item

    def __setitem__(self, key, value):
        if not isinstance(key, tuple):
            key = (key,)
        item = self._ndict
        for k in key[:-1]:
            item = item.setdefault(k, {})
        item[key[-1]] = value

    def __delitem__(self, key):
        """Deletes item, then looks at the level above and checks if it contains an empty dictionary"""
        if not isinstance(key, tuple):
            key = (key,)
        new_key, last_key = key[:-1], key[-1]
        del self[new_key][last_key]

        if (new_key != ()) & (self[new_key] == {}):
            self.__delitem__(new_key)

    def __iter__(self):
        def wrapped(ndict, key=[]):
            if not isinstance(ndict, dict):
                yield tuple(key)
            else:
                for node, branch in ndict.items():
                    key.append(node)
                    yield from wrapped(branch, key)
                    key.pop()

        return wrapped(self._ndict)

    def __len__(self):
        """Number of keys in the nested dictionary"""
        len = 0
        for _ in self:
            len += 1
        return len

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self._ndict})"

    @property
    def extract(self):
        """Extracts item as a NestedDict"""
        return _Extractor(self)

    def copy(self):
        return deepcopy(self)

    def to_dict(self):
        return deepcopy(self._ndict)


class _Extractor:
    """Class that allows methods of other classes to have square brackets"""

    def __init__(self, extractee):
        self._extractee = extractee

    def __getitem__(self, key):
        """Where _extractee would only return the value for a given key,
        this method returns a new _exctractee instance including the key as well.

        An empty string means all keys are chosen"""
        if type(key) is not tuple:
            key = (key,)
        item = self._extractee.__class__()

        if "" in key:
            for self_key in self._extractee.keys():
                if len(self_key) < len(key):
                    continue
                for k, s_k in zip(key, self_key):
                    if k == "":
                        continue
                    elif k != s_k:
                        break
                else:
                    item[self_key] = self._extractee[self_key]
        else:
            item[key] = self._extractee[key]

        return item


class Arithmetics(ABC):
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


class DataDict(NestedDict, Arithmetics):
    """A NestedDict that supports arithmetics.
    Other methods are included that make DataDict similar to DataFrames"""

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
        """Apply func to all values"""
        if inplace:
            for key, leaf in self.items():
                self[key] = func(leaf)
        else:
            new_self = self.copy()
            for key, leaf in new_self.items():
                new_self[key] = func(leaf)
            return new_self

    def reduce(self, func: Callable, *initial: Any):
        """Pass func and initial to functools.reduce and apply it to all values"""
        return reduce(func, self.values(), *initial)

    def total(self):
        """Returns sum of all values"""
        return sum(self.values())

    def mean(self) -> Number:
        """Returns mean of all values"""
        return self.total() / len(self)

    def std(self) -> Number:
        """Returns standard deviation of all values"""
        step = self.reduce(lambda a, b: a + (b - self.mean()) ** 2, 0)
        step /= len(self) - 1
        return step**0.5


if __name__ == "__main__":

    farm_data = {
        "T1": {
            "blade": {"Mx": 10, "My": 0.9, "Mz": 2},
            "tower": {"Mx": 4, "My": 0.85, "Mz": 3},
        },
        "T2": {
            "tower": {"Mx": 4, "My": 0.0, "Mz": 4},
            "gearbox": {
                "Mx": {"sensor_1": 2, "sensor_2": 1},
                "My": {"sensor_1": 2, "sensor_2": 1},
            },
        },
    }

    # Initialise class from a nested dictionary
    farm = NestedProperty(farm_data)

    # Use CartesianInit to initialise from lists
    turbines = ["T" + str(i) for i in range(1, 11)]
    components = ["blade", "tower", "gearbox"]
    loads = ["Mx", "My", "Mz"]
    limits = ["Central", "Lower", "Upper"]
    other_farm = NestedProperty.from_product(turbines, components, loads, limits)
    print(other_farm)

    # Loop over values, keys (the path to a leaf), or both
    print(">>> Loops")
    for leaf in farm.values():
        print(leaf)

    for key, leaf in farm.items():
        print(key, leaf)

    for key in farm.keys():
        print(key)

    for leaf in farm:
        print(leaf)

    # Check if a value is present in the values
    print(">>> is key in NestedDict?")
    first_key = list(farm.keys())[0]
    assert first_key in farm

    # Trees are printed as nested dictionaries
    print(">>> print")
    print(farm)

    # Number of values
    print(">>> length")
    print(len(farm))

    # Assign new value
    farm["T1", "blade", "Mx"] = 14
    # Create item if it doesn't exist
    farm["T100", "blade", "Mx"] = 14
    # Delete item
    del farm["T100", "blade", "Mx"]

    # Use tuples to access values
    assert farm["T2", "tower", "Mx"] == farm_data["T2"]["tower"]["Mx"]
    # This makes iterating through the data easier,
    # no nested for loops as in nested dictionaries,
    # no masks as in dataframes, ie farm[(farm[turbine] == "T1") & ...]
    my_func = lambda x: x
    for key, leaf in farm.items():
        farm[key] = my_func(leaf)

    # Extract data as a NestedDictionary
    turbine1 = farm.extract["T1"]
    turbine1_blade = farm.extract["T1", "blade"]
    all_blades = farm.extract["", "tower"]
    # Apply the same function to all values, as in dataframes
    farm.apply(lambda x: x + 1, inplace=True)

    # Logic operations
    print(">>> != and ==")
    print(farm != 1)
    print(farm == farm)

    # Deep copy
    farm2 = farm.copy()
    farm2["T1", "blade", "Mx"] = 10
    assert farm != farm2

    # Operations on all the values which return a single value
    print(">>> total, mean and std")
    print(farm.total())
    print(farm.mean())
    print(farm.std())

    # Arithmetics between trees that share the same keys
    print(">>> Arithmetics")
    print(farm + farm)
    print(-farm)
    print(farm - farm)
    print(farm + 1)
    print(farm - 1)

    print(farm)
    print(farm * 2)
    farm += 1
    print(farm / 10)

    print(">>> Methods inherited by MutableMapping")
    print(farm.popitem())
    farm["T100"] = 0
    print(farm.pop("T100"))
    print(farm.get("T100", "get default"))
    print(farm.setdefault("T100", {"blade": {"Mx": 1}}))
