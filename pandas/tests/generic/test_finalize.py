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
]


@pytest.fixture(params=_all_methods)
def ndframe_method(request):
    """
    An NDFrame method returning an NDFrame.
    """
    return request.param


def test_finalize_called(ndframe_method):
    cls, init_args, method = ndframe_method
    ndframe = cls(*init_args)

    ndframe.attrs = {"a": 1}
    result = method(ndframe)

    assert result.attrs == {"a": 1}


# TODO: groupby
