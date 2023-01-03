First of all import `NestedDict`, the main data structure of `ndicts`.

```pycon
>>> from ndicts import NestedDict
```

Create a `NestedDict` from a nested dictionary.

```pycon
>>> d = {"a": {"aa": {"aaa": 0}}, "b": {"ba": 1}}
>>> nd = NestedDict(d)
```

Access deeper levels with an easier syntax than that of dictionaries.

```pycon
>>> # NestedDict
>>> nd["a", "aa", "aaa"]
0
>>> # dict
>>> d["a"]["aa"]["aaa"]
0
```

Iterate over leaf values and their keys.

```pycon
>>> for key in nd:
...     print(key)
('a', 'aa', 'aaa')
('b', 'ba')
>>> for value in nd.values():
...     print(value)
0
1
```

See the [API reference](nested_dict.md) for more examples.
