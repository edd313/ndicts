The default method to initialize a `NestedDict` is from a `dict`.

```pycon
>>> nd = NestedDict{"a": {"x": 0, "y": 0}, "b": {"x": 0, "y": 0}}
```

It is possible to initialize by passing the keys as tuples.

```pycon
>>> keys = [("a", "x"), ("a", "y"), ("b", "x"), ("b", "y")]
>>> NestedDict.from_tuples(*keys, value=0)
NestedDict{"a": {"x": 0, "y": 0}, "b": {"x": 0, "y": 0}}
```

In this case, the same results can be obtained by cartesian product.

```pycon
>>> levels = [("a", "b"), ("x", "y")]
>>> NestedDict.from_product(*levels, value=0)
NestedDict{"a": {"x": 0, "y": 0}, "b": {"x": 0, "y": 0}}
```
