"""Tests for the DataDict class."""

import pytest

from ndicts import DataDict, NestedDict
from ndicts.data_dict import _Arithmetics


@pytest.fixture
def dd():
    return DataDict.from_product(["ab", "ab"], values=1)


def test_inheritance():
    assert isinstance(DataDict(), (NestedDict, _Arithmetics))


def test_arithmetics():
    iterables = ["ab", "ab"]
    v1, v2 = 1, 2
    dd1 = DataDict.from_product(iterables, values=v1)
    dd2 = DataDict.from_product(iterables, values=v2)

    assert dd1 + dd2 == DataDict.from_product(iterables, values=v1 + v2)
    assert dd2 + dd1 == DataDict.from_product(iterables, values=v1 + v2)
    assert dd1 - dd2 == DataDict.from_product(iterables, values=v1 - v2)
    assert dd2 - dd1 == DataDict.from_product(iterables, values=v2 - v1)
    assert dd1 * dd2 == DataDict.from_product(iterables, values=v1 * v2)
    assert dd2 * dd1 == DataDict.from_product(iterables, values=v1 * v2)
    assert dd1 / dd2 == DataDict.from_product(iterables, values=v1 / v2)
    assert dd2 / dd1 == DataDict.from_product(iterables, values=v2 / v1)
    assert dd1**dd2 == DataDict.from_product(iterables, values=v1**v2)
    assert dd2**dd1 == DataDict.from_product(iterables, values=v2**v1)
    assert dd1 // dd2 == DataDict.from_product(iterables, values=v1 // v2)
    assert dd2 // dd1 == DataDict.from_product(iterables, values=v2 // v1)
    assert dd1 % dd2 == DataDict.from_product(iterables, values=v1 % v2)
    assert dd2 % dd1 == DataDict.from_product(iterables, values=v2 % v1)


def test_arithmetics_extract(dd):
    """Extract a DataDict, and perform an operation back with the original one."""
    dd_extract = dd.extract["", "b"]
    assert dd - dd_extract == DataDict({"a": {"a": 1, "b": 0}, "b": {"a": 1, "b": 0}})

    dd = DataDict.from_product(["ab", "ab"], values=2)
    dd_extract = dd.extract["a"]
    assert dd * dd_extract == DataDict({"a": {"a": 4, "b": 4}, "b": {"a": 2, "b": 2}})


def test_apply(dd):
    assert dd.apply(lambda x: 2 * x + 1) == DataDict.from_product(["ab", "ab"], values=3)
    dd.apply(lambda x: 2 * x + 1, inplace=True)
    assert dd == DataDict.from_product(["ab", "ab"], values=3)


def test_reduce(dd):
    assert dd.reduce(lambda x, y: x + y) == sum(dd.values())
    assert dd.reduce(lambda x, y: x + y, 3) == sum(dd.values()) + 3


def test_total(dd):
    assert dd.total() == 4


def test_mean(dd):
    assert dd.mean() == 1


def test_std(dd):
    assert dd.std() == 0
