from collections.abc import MutableMapping
from copy import deepcopy
from itertools import product
from typing import Any, Generator, Iterable, List, Tuple, TypeVar, Union

from more_itertools import zip_equal

T = TypeVar('T', bound='Parent')


class NestedDict(MutableMapping):
    """Nested dictionary data structure.

    Handle nested dictionaries with an interface
    similar to standard dictionaries.

    Args:
        dictionary (dict): Input nested dictionary.
        copy (bool): Set to True to copy the input dictionary.

    See Also:
        NestedDict.from_product: Initialize from cartesian product.

        NestedDict.from_tuples: Initialize from list of tuples.

    Examples:
        Initialize from a nested dictionary.

        >>> d = {"a": {"a": 0, "b": 1}, "b": 2}
        >>> nd = NestedDict(d)
        >>> nd
        NestedDict({'a': {'a': 0, 'b': 1}, 'b': 2})

        Get an item.

        >>> nd["a"]
        {'a': 0, 'b': 1}
        >>> nd[("a", "b")]
        1

        Set an item.

        >>> nd[("c", "a")] = 3
        >>> nd
        NestedDict({'a': {'a': 0, 'b': 1}, 'b': 2, 'c': {'a': 3}})

        Delete an item.

        >>> del nd["c"]
        >>> nd
        NestedDict({'a': {'a': 0, 'b': 1}, 'b': 2})

        Iterate over keys.

        >>> [key for key in nd]
        [('a', 'a'), ('a', 'b'), ('b',)]
        >>> [key for key in nd.keys()]
        [('a', 'a'), ('a', 'b'), ('b',)]

        Iterate over values.

        >>> [value for value in nd.values()]
        [0, 1, 2]

        Iterate over items.

        >>> [item for item in nd.items()]
        [(('a', 'a'), 0), (('a', 'b'), 1), (('b',), 2)]
    """

    @classmethod
    def from_tuples(cls, tuples: List[Iterable], values: Union[Any, Iterable] = None) -> T:
        """Initialize a NestedDict from a list of iterables.

        Args:
            tuples:
                Tuples corresponding to the keys of the NestedDict.
            values:
                If values is an iterable but not a string,
                its values will become to those of the NestedDict.
                If a non-iterable or string is passed,
                it will be assigned to each value of the NestedDict.

        Returns:
            NestedDict

        Raises:
            UnequalIterablesError: If the keys and values have different length.

        Examples:
            >>> tuples = [("a", "aa"), ("b",)]
            >>> NestedDict.from_tuples(tuples)
            NestedDict({'a': {'aa': None}, 'b': None})

            Initialize with a single value.

            >>> NestedDict.from_tuples(tuples, values=0)
            NestedDict({'a': {'aa': 0}, 'b': 0})

            Initialize with different values.

            >>> NestedDict.from_tuples(tuples, values=[0, 1])
            NestedDict({'a': {'aa': 0}, 'b': 1})

            Passing values with the wrong size will throw an exception.

            >>> NestedDict.from_tuples(tuples, values=range(99))
            Traceback (most recent call last):
            ...
            more_itertools.recipes.UnequalIterablesError: Iterables have different lengths...
        """
        nd = cls()
        if isinstance(values, Iterable) and not isinstance(values, str):
            for key, value in zip_equal(tuples, values):
                nd[key] = value
        else:
            for key in tuples:
                nd[key] = values
        return nd

    @classmethod
    def from_product(cls, iterables: List[Iterable], values: Union[Any, Iterable] = None) -> T:
        """Initialize a NestedDict by cartesian product.

        Args:
            iterables:
                Input iterables.
            values:
                If values is an iterable but not a string,
                it will be assigned to the values of the NestedDict.
                If a non-iterable or string is passed,
                it will be assigned to each value of the NestedDict.

        Returns:
            NestedDict

        Raises:
            UnequalIterablesError: If the keys and values have different length.

        Examples:
            >>> iterables = [("A", "B"), ("a", "b")]
            >>> NestedDict.from_product(iterables)
            NestedDict({'A': {'a': None, 'b': None}, 'B': {'a': None, 'b': None}})

            Initialize with a single value.

            >>> NestedDict.from_product(iterables, values=0)
            NestedDict({'A': {'a': 0, 'b': 0}, 'B': {'a': 0, 'b': 0}})

            Initialize with different values.

            >>> NestedDict.from_product(iterables, values=[0, 1, 2, 3])
            NestedDict({'A': {'a': 0, 'b': 1}, 'B': {'a': 2, 'b': 3}})

            Passing values with the wrong size will throw an exception.

            >>> NestedDict.from_product(iterables, values=range(99))
            Traceback (most recent call last):
            ...
            more_itertools.recipes.UnequalIterablesError: Iterables have different lengths
        """
        keys = product(*iterables)
        return cls.from_tuples(keys, values)

    def __init__(self, dictionary: dict = None, copy: bool = False) -> None:
        """Initialize a NestedDict from a dictionary.
        
        See class docstring.
        """
        if dictionary is None:
            dictionary = {}
        self._ndict = deepcopy(dictionary) if copy else dictionary

    def __getitem__(self, key: Union[Any, Tuple]) -> Any:
        """Get item associated to the key.

        Args:
            key:
                Either comma-separated values or tuples.

        Returns:
            Value associated to the key.

        Raises:
            KeyError: If the key does not belong to the NestedDict.

        Examples:
            >>> d = {"a": {"a": 0, "b": 1}}
            >>> nd = NestedDict(d)

            Get the first level.

            >>> nd["a"]
            {'a': 0, 'b': 1}

            Get a deeper value.

            >>> nd["a", "a"]
            0

            Tuples can be passed too.
            >>> nd[("a", "b")]
            1

            An exception is thrown if they key does not exist.

            >>> nd["z"]
            Traceback (most recent call last):
            ...
            KeyError: ('z',)
        """
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

    def __setitem__(self, key: Union[Any, Tuple], value: Any) -> None:
        """Set the key to the given value.

        If the key does not exist it is created.

        Args:
            key: Key to be set.
            value: New value for the key.

        Examples:
            Set an existing key.

            >>> nd = NestedDict({"a": {"aa": 0}})
            >>> nd["a", "aa"] = 1
            >>> nd
            NestedDict({'a': {'aa': 1}})

            Set a new key.
            >>> nd["a", "ab"] = 2
            >>> nd
            NestedDict({'a': {'aa': 1, 'ab': 2}})
        """
        if not isinstance(key, tuple):
            key = (key,)
        item = self._ndict
        for k in key[:-1]:
            item = item.setdefault(k, {})
        item[key[-1]] = value

    def __delitem__(self, key: Union[Any, Tuple]) -> None:
        """Delete item corresponding to the key.

        If the levels above are left empty, they are deleted.

        Args:
            key: Key as defined in NestedDict.__getitem__

        Examples:
            >>> d = {"a": {"aa": {"aaa": 0}}, "b": 1}
            >>> nd = NestedDict(d)
            >>> del nd["b"]
            >>> nd
            NestedDict({'a': {'aa': {'aaa': 0}}})

            Levels which are left empty after deleting an item are deleted too.

            >>> del nd["a", "aa", "aaa"]
            >>> nd
            NestedDict({})
        """
        if not isinstance(key, tuple):
            key = (key,)
        new_key, last_key = key[:-1], key[-1]
        del self[new_key][last_key]

        if (new_key != ()) & (self[new_key] == {}):
            self.__delitem__(new_key)

    def __iter__(self) -> Generator:
        """Iterate over a NestedDict.

        Yield only the keys that are associated to a leaf value.

        Note:
            NestedDict is a MutableMapping, thus it is possible
            to iterate over values, keys and items exactly as a dictionary.
            See the examples.

        Examples:
            >>> d = {"a": {"aa": 0, "ab": 1}, "b": 2}
            >>> nd = NestedDict(d)
            >>> [key for key in nd]
            [('a', 'aa'), ('a', 'ab'), ('b',)]

            Alternative to iterate over the keys.

            >>> [key for key in nd.keys()]
            [('a', 'aa'), ('a', 'ab'), ('b',)]

            Iterate over the leaf values.

            >>> [value for value in nd.values()]
            [0, 1, 2]

            Iterate over the items.
            >>> [item for item in nd.items()]
            [(('a', 'aa'), 0), (('a', 'ab'), 1), (('b',), 2)]
        """
        def wrapped(ndict, key=[]):
            """Traverse the nested dictionary recursively.

            Yield the key once a leaf value is reached.
            """
            if not isinstance(ndict, dict):
                yield tuple(key)
            else:
                for node, branch in ndict.items():
                    key.append(node)
                    yield from wrapped(branch, key)
                    key.pop()

        return wrapped(self._ndict)

    def __len__(self) -> int:
        """Number of leaf values.

        Examples:
            >>> nd = NestedDict({"a": {"aa": 0, "ab": 0}, "b": 0})
            >>> len(nd)
            3
        """
        length = 0
        for _ in self:
            length += 1
        return length

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self._ndict})"

    @property
    def extract(self):
        """Get item as a NestedDict.

        Instead of a dict or a value, a NestedDict is returned.
        The method can be used for filtering.
        An empty string "" can be used as a wildcard to match all levels.

        Examples:
             >>> nd = NestedDict.from_product(["ab", "xy"], values=0)
             >>> nd
             NestedDict({'a': {'x': 0, 'y': 0}, 'b': {'x': 0, 'y': 0}})
             >>> nd.extract["a"]
             NestedDict({'a': {'x': 0, 'y': 0}})

             Use the wildcard to extract all items with "x" on the second level.
             >>> nd.extract["", "x"]
             NestedDict({'a': {'x': 0}, 'b': {'x': 0}})
        """
        return _Extractor(self)

    def rows(self) -> Generator:
        """Yield the NestedDict row by row.

        A row is obtained by adding the leaf value
        to the sequence of its key.

        Notes:
            This method can be useful to export
            a NestedDict to a pandas DataFrame.

        Yields:
            A row of the NestedDict.

        Examples:
            >>> nd = NestedDict({"a": 0, "b": {"ba": 1}, "c": 2})
            >>> [row for row in nd.rows()]
            [('a', 0), ('b', 'ba', 1), ('c', 2)]
        """
        return ((*key, value) for key, value in self.items())

    def copy(self) -> T:
        """Return a deep copy."""
        return deepcopy(self)

    def to_dict(self) -> dict:
        """Return a copy as a dictionary."""
        return deepcopy(self._ndict)


class _Extractor:
    """Class that allows methods of other classes to have square brackets."""

    def __init__(self, extractee):
        self._extractee = extractee

    def __getitem__(self, key):
        """Returns a new _exctractee instance including the key as well.

        An empty string means all keys are chosen.
        """
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



