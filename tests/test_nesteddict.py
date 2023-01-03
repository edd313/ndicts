"""Tests for the NestedDict class"""

from itertools import product
import pytest
from ndicts import __version__
from ndicts import NestedDict


def test_init():
    d = {"a": {"a": 0, "b": 0}, "b": {"a": 0, "b": 0}}
    assert NestedDict(d) == NestedDict.from_product(["a", "b"], ["a", "b"], value=0)


def test_init_classmethods():
    iterables = [["a", "b"], ["x", "y"], ["u", "v"]]
    tuples = list(product(*iterables))

    assert NestedDict.from_product(*iterables) == NestedDict.from_tuples(*tuples)
    assert NestedDict.from_product(*iterables, value=0) == NestedDict.from_tuples(
        *tuples, value=0
    )


def test_getitem():
    nd = NestedDict({"a": {"a": 0}})
    assert nd["a", "a"] == 0

    with pytest.raises(KeyError):
        nd["z"]


def test_contains():
    nd = NestedDict({"a": {"a": 0}})

    assert ("a", "a") in nd
    assert ("b",) not in nd


def test_setitem():
    nd = NestedDict()
    nd["a", "a", "a"] = 0
    nd["a", "b", "a"] = 1

    assert nd["a", "a", "a"] == 0
    assert nd["a", "b", "a"] == 1


def test_delitem():
    nd = NestedDict()
    nd["a", "a", "a"] = 0
    nd["a", "b", "a"] = 1
    nd["b", "a"] = 2
    nd["b", "b"] = 2

    del nd["a", "a", "a"]
    assert ("a", "a", "a") not in nd

    del nd["a", "b"]
    assert ("a",) not in nd

    del nd["b"]
    assert nd == NestedDict()


def test_iter():
    iterables = [["a", "b"], ["x", "y"]]
    keys = list(product(*iterables))
    nd = NestedDict.from_product(*iterables)
    for key in nd:
        assert key in keys


def test_iter_keys():
    iterables = [["a", "b"], ["x", "y"]]
    keys = list(product(*iterables))
    nd = NestedDict.from_product(*iterables)
    for key in nd.keys():
        assert key in keys


def test_iter_values():
    iterables = [["a", "b"], ["x", "y"]]
    nd = NestedDict.from_product(*iterables)
    for value in nd.values():
        assert value is None


def test_iter_items():
    iterables = [["a", "b"], ["x", "y"]]
    keys = list(product(*iterables))
    nd = NestedDict.from_product(*iterables)
    for key, value in nd.items():
        assert key in keys
        assert value is None


def test_len():
    assert len(NestedDict()) == 0
    assert len(NestedDict.from_product("ab", "ab")) == 4


def test_bool():
    assert bool(NestedDict()) is False
    assert bool(NestedDict.from_tuples("a")) is True


def test_str():
    nd = NestedDict.from_tuples("a")
    assert nd == eval(str(nd))


def test_extract():
    nd = NestedDict.from_product("ab", "xy")
    assert nd.extract["a"] == NestedDict.from_product("a", "xy")
    assert nd.extract["", "x"] == NestedDict.from_product("ab", "x")


def test_copy():
    nd = NestedDict.from_tuples(("a", "a"), ("a", "b"))
    nd_copy = nd.copy()
    assert nd == nd_copy
    assert nd is not nd_copy


def test_to_dict():
    d = {"a": {"a": 0, "b": 1}, "b": 2}
    nd = NestedDict(d)
    assert nd.to_dict() == d
    assert nd.to_dict()["a"] == d["a"]


def test_version():
    assert __version__ == "0.2.1"


if __name__ == "__main__":
    test_init()
