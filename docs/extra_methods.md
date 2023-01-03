`NestedDict` is a `MutableMapping`, which means that all dictionary methods are available. The methods that are not described in the docstrings are documented here.

The following `NestedDict` is used for all the examples below.

```pycon
>>> nd = NestedDict({"a": {"aa": 0}, "b": 1})
```

## \_\_contains__

```pycon
>>> "a" in nd
True
>>> ("a", "aa") in nd
True
>>> "x" in nd
False
```

## \_\_eq__, \_\_ne__

```pycon
>>> nd == nd
True
>>> nd == NestedDict({'b': 1})
False
>>> nd != NestedDict({'b': 1})
True
```

## get

```pycon
>>> nd.get("a")
{'aa': 0}
>>> nd.get("x", "not present")
'not present'
>>> nd
NestedDict({'a': {'aa': 0}, 'b': 1})
```

## setdefault

```pycon
>>> nd.setdefault("a")
{'aa': 0}
>>> nd.setdefault("x", "now present")
'now present'
>>> nd
NestedDict({'a': {'aa': 0}, 'b': 1, 'x': 'now present'})
```

## pop

```pycon
>>> nd.pop("x")
'now present'
>>> nd
NestedDict({'a': {'aa': 0}, 'b': 1)
```

## popitem

```pycon
>>> nd.popitem()
(('a', 'aa'), 0)
>>> nd
NestedDict({'b': 1})
```

## update

```pycon
>>> nd.update(NestedDict({"a": {"aa": 0}, "b": 1}))
>>> nd
NestedDict({'b': 1, 'a': {'aa': 0}})
```

## clear

```pycon
>>> nd.clear()
>>> nd
NestedDict({})
```
