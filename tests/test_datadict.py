"""Tests for the DataDict class"""

from ndicts.ndicts import Arithmetics, DataDict, NestedDict


def test_inheritance():
    assert isinstance(DataDict(), (NestedDict, Arithmetics))


def test_arithmetics():
    iterables = ["ab", "ab"]
    v1, v2 = 1, 2
    dd1 = DataDict.from_product(*iterables, value=v1)
    dd2 = DataDict.from_product(*iterables, value=v2)

    assert dd1 + dd2 == DataDict.from_product(*iterables, value=v1 + v2)
    assert dd2 + dd1 == DataDict.from_product(*iterables, value=v1 + v2)
    assert dd1 - dd2 == DataDict.from_product(*iterables, value=v1 - v2)
    assert dd2 - dd1 == DataDict.from_product(*iterables, value=v2 - v1)
    assert dd1 * dd2 == DataDict.from_product(*iterables, value=v1 * v2)
    assert dd2 * dd1 == DataDict.from_product(*iterables, value=v1 * v2)
    assert dd1 / dd2 == DataDict.from_product(*iterables, value=v1 / v2)
    assert dd2 / dd1 == DataDict.from_product(*iterables, value=v2 / v1)
    assert dd1**dd2 == DataDict.from_product(*iterables, value=v1**v2)
    assert dd2**dd1 == DataDict.from_product(*iterables, value=v2**v1)
    assert dd1 // dd2 == DataDict.from_product(*iterables, value=v1 // v2)
    assert dd2 // dd1 == DataDict.from_product(*iterables, value=v2 // v1)
    assert dd1 % dd2 == DataDict.from_product(*iterables, value=v1 % v2)
    assert dd2 % dd1 == DataDict.from_product(*iterables, value=v2 % v1)


def test_arithmetics_extract():
    """Extract a DataDict, and perform an operation back with the original one"""
    dd = DataDict.from_product("ab", "ab", value=2)
    dd_extract = dd.extract["", "b"]
    assert dd - dd_extract == DataDict({"a": {"a": 2, "b": 0}, "b": {"a": 2, "b": 0}})

    dd = DataDict.from_product("ab", "ab", value=2)
    dd_extract = dd.extract["a"]
    assert dd * dd_extract == DataDict({"a": {"a": 4, "b": 4}, "b": {"a": 2, "b": 2}})


def test_apply():
    dd = DataDict.from_product("ab", "ab", value=1)
    assert dd.apply(lambda x: 2 * x + 1) == DataDict.from_product("ab", "ab", value=3)
    dd.apply(lambda x: 2 * x + 1, inplace=True)
    assert dd == DataDict.from_product("ab", "ab", value=3)


def test_reduce():
    dd = DataDict.from_product("ab", "ab", value=1)
    assert dd.reduce(lambda x, y: x + y) == sum(dd.values())
    assert dd.reduce(lambda x, y: x + y, 3) == sum(dd.values()) + 3


def test_total():
    dd = DataDict.from_product("ab", "ab", value=1)
    assert dd.total() == 4


def test_mean():
    dd = DataDict.from_product("ab", "ab", value=1)
    assert dd.mean() == 1


def test_std():
    dd = DataDict.from_product("ab", "ab", value=1)
    assert dd.std() == 0
