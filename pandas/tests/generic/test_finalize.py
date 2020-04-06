import operator

import pytest

import pandas as pd

mi = pd.MultiIndex.from_product([["a", "b"], [0, 1]], names=["A", "B"])


_all_methods = [
    (pd.Series, [0], operator.methodcaller("view", int)),
    (pd.Series, [0], operator.methodcaller("take", [])),
    (pd.Series, [0], operator.methodcaller("__getitem__", [True])),
    (pd.Series, [0], operator.methodcaller("repeat", 2)),
    pytest.param(
        (pd.Series, [0], operator.methodcaller("reset_index")), marks=pytest.mark.xfail
    ),
    (pd.Series, [0], operator.methodcaller("reset_index", drop=True)),
    pytest.param(
        (pd.Series, [0], operator.methodcaller("to_frame")), marks=pytest.mark.xfail
    ),
    (pd.Series, (0, mi), operator.methodcaller("count", level="A")),
    (pd.Series, ([0, 0],), operator.methodcaller("drop_duplicates")),
    (pd.Series, ([0, 0],), operator.methodcaller("duplicated")),
    (pd.Series, ([0, 0],), operator.methodcaller("round")),
    (pd.Series, ([0, 0],), operator.methodcaller("rename", lambda x: x + 1)),
    (pd.Series, ([0, 0],), operator.methodcaller("rename", "name")),
    (pd.Series, ([0, 0],), operator.methodcaller("set_axis", ["a", "b"])),
    (pd.Series, ([0, 0],), operator.methodcaller("reindex", [1, 0])),
    (pd.Series, ([0, 0],), operator.methodcaller("drop", [0])),
    (pd.Series, (pd.array([0, pd.NA]),), operator.methodcaller("fillna", 0)),
    (pd.Series, ([0, 0],), operator.methodcaller("replace", {0: 1})),
    (pd.Series, ([0, 0],), operator.methodcaller("shift")),
    (pd.Series, ([0, 0],), operator.methodcaller("isin", [0, 1])),
    (pd.Series, ([0, 0],), operator.methodcaller("between", 0, 2)),
    (pd.Series, ([0, 0],), operator.methodcaller("isna")),
    (pd.Series, ([0, 0],), operator.methodcaller("isnull")),
    (pd.Series, ([0, 0],), operator.methodcaller("notna")),
    (pd.Series, ([0, 0],), operator.methodcaller("notnull")),
    (
        pd.Series,
        ([0], pd.period_range("2000", periods=1)),
        operator.methodcaller("to_timestamp"),
    ),
    (
        pd.Series,
        ([0], pd.date_range("2000", periods=1)),
        operator.methodcaller("to_period"),
    ),
]


@pytest.fixture(params=_all_methods)
def ndframe_method(request):
    """
    An NDFrame method returning an NDFrame.
    """
    return request.param


@pytest.mark.parametrize(
    "method",
    [
        operator.methodcaller("upper"),
        pytest.param(
            operator.methodcaller("extract", r"(\w)(\d)"),
            marks=pytest.mark.xfail(reason="finalize not called."),
        ),
    ],
)
def test_string_method(method):
    s = pd.Series(["a1"])
    s.attrs = {"a": 1}
    result = method(s.str)
    assert result.attrs == {"a": 1}


@pytest.mark.xfail(reason="TODO")
def test_datetime_method():
    s = pd.Series(pd.date_range("2000", periods=4))
    s.attrs = {"a": 1}
    result = s.dt.date
    assert result.attrs == {"a": 1}


def test_finalize_called(ndframe_method):
    cls, init_args, method = ndframe_method
    ndframe = cls(*init_args)

    ndframe.attrs = {"a": 1}
    result = method(ndframe)

    assert result.attrs == {"a": 1}


# TODO: groupby
