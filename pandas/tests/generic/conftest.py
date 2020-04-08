import operator
import re

import numpy as np
import pytest

import pandas as pd

not_implemented_mark = pytest.mark.xfail(reason="__finalize__ not implemented")

mi = pd.MultiIndex.from_product([["a", "b"], [0, 1]], names=["A", "B"])

frame_data = ({"A": [1]},)
frame_mi_data = ({"A": [1, 2, 3, 4]}, mi)


# Tuple of
# - Callable: Constructor (Series, DataFrame)
# - Tuple: Constructor args
# - Callable: pass the constructed value with attrs set to this.

all_methods = [
    (pd.Series, ([0],), operator.methodcaller("view", int)),
    (pd.Series, ([0],), operator.methodcaller("take", [])),
    (pd.Series, ([0],), operator.methodcaller("__getitem__", [True])),
    (pd.Series, ([0],), operator.methodcaller("repeat", 2)),
    pytest.param(
        (pd.Series, ([0],), operator.methodcaller("reset_index")),
        marks=pytest.mark.xfail,
    ),
    (pd.Series, ([0],), operator.methodcaller("reset_index", drop=True)),
    pytest.param(
        (pd.Series, ([0],), operator.methodcaller("to_frame")), marks=pytest.mark.xfail
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
    (pd.Series, ([1],), operator.methodcaller("add", pd.Series([1]))),
    # TODO: mul, div, etc.
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
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("dot", pd.DataFrame(index=["A"])),
        ),
        marks=pytest.mark.xfail(reason="Implement binary finalize"),
    ),
    (pd.DataFrame, frame_data, operator.methodcaller("transpose")),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("__getitem__", "A")),
        marks=not_implemented_mark,
    ),
    (pd.DataFrame, frame_data, operator.methodcaller("__getitem__", ["A"])),
    (pd.DataFrame, frame_data, operator.methodcaller("__getitem__", np.array([True]))),
    (pd.DataFrame, ({("A", "a"): [1]},), operator.methodcaller("__getitem__", ["A"])),
    (pd.DataFrame, frame_data, operator.methodcaller("query", "A == 1")),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("eval", "A + 1")),
        marks=not_implemented_mark,
    ),
    (pd.DataFrame, frame_data, operator.methodcaller("select_dtypes", include="int")),
    (pd.DataFrame, frame_data, operator.methodcaller("assign", b=1)),
    (pd.DataFrame, frame_data, operator.methodcaller("set_axis", ["A"])),
    (pd.DataFrame, frame_data, operator.methodcaller("reindex", [0, 1])),
    (pd.DataFrame, frame_data, operator.methodcaller("drop", columns=["A"])),
    (pd.DataFrame, frame_data, operator.methodcaller("drop", index=[0])),
    (pd.DataFrame, frame_data, operator.methodcaller("rename", columns={"A": "a"})),
    (pd.DataFrame, frame_data, operator.methodcaller("rename", index=lambda x: x)),
    (pd.DataFrame, frame_data, operator.methodcaller("fillna", "A")),
    (pd.DataFrame, frame_data, operator.methodcaller("fillna", method="ffill")),
    (pd.DataFrame, frame_data, operator.methodcaller("set_index", "A")),
    (pd.DataFrame, frame_data, operator.methodcaller("reset_index")),
    (pd.DataFrame, frame_data, operator.methodcaller("isna")),
    (pd.DataFrame, frame_data, operator.methodcaller("isnull")),
    (pd.DataFrame, frame_data, operator.methodcaller("notna")),
    (pd.DataFrame, frame_data, operator.methodcaller("notnull")),
    (pd.DataFrame, frame_data, operator.methodcaller("dropna")),
    (pd.DataFrame, frame_data, operator.methodcaller("drop_duplicates")),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("duplicated")),
        marks=not_implemented_mark,
    ),
    (pd.DataFrame, frame_data, operator.methodcaller("sort_values", by="A")),
    (pd.DataFrame, frame_data, operator.methodcaller("sort_index")),
    (pd.DataFrame, frame_data, operator.methodcaller("nlargest", 1, "A")),
    (pd.DataFrame, frame_data, operator.methodcaller("nsmallest", 1, "A")),
    (pd.DataFrame, frame_mi_data, operator.methodcaller("swaplevel"),),
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("add", pd.DataFrame(*frame_data)),
        ),
        marks=not_implemented_mark,
    ),
    # TODO: div, mul, etc.
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("combine", pd.DataFrame(*frame_data)),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("combine_first", pd.DataFrame(*frame_data)),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("update", pd.DataFrame(*frame_data)),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("pivot", columns="A")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            {"A": [1], "B": [1]},
            operator.methodcaller("pivot_table", columns="A"),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("stack")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("explode", "A")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_mi_data, operator.methodcaller("unstack"),),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            ({"A": ["a", "b", "c"], "B": [1, 3, 5], "C": [2, 4, 6]},),
            operator.methodcaller("melt", id_vars=["A"], value_vars=["B"]),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("diff")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("applymap", lambda x: x)),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("append", pd.DataFrame({"A": [1]})),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("append", pd.DataFrame({"B": [1]})),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("merge", pd.DataFrame({"A": [1]})),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("round", 2)),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("corr")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("cov")),
        marks=[
            not_implemented_mark,
            pytest.mark.filterwarnings("ignore::RuntimeWarning"),
        ],
    ),
    pytest.param(
        (
            pd.DataFrame,
            frame_data,
            operator.methodcaller("corrwith", pd.DataFrame(*frame_data)),
        ),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("count")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_mi_data, operator.methodcaller("count", level="A")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("nunique")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("idxmin")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("idxmax")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("mode")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("quantile")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("quantile", q=[0.25, 0.75])),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("quantile")),
        marks=not_implemented_mark,
    ),
    (
        pd.DataFrame,
        ({"A": [1]}, [pd.Period("2000", "D")]),
        operator.methodcaller("to_timestamp"),
    ),
    (
        pd.DataFrame,
        ({"A": [1]}, [pd.Timestamp("2000")]),
        operator.methodcaller("to_period", freq="D"),
    ),
    pytest.param(
        (pd.DataFrame, frame_mi_data, operator.methodcaller("isin", [1])),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_mi_data, operator.methodcaller("isin", pd.Series([1]))),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (
            pd.DataFrame,
            frame_mi_data,
            operator.methodcaller("isin", pd.DataFrame({"A": [1]})),
        ),
        marks=not_implemented_mark,
    ),
    (pd.DataFrame, frame_data, operator.methodcaller("swapaxes", 0, 1)),
    (pd.DataFrame, frame_mi_data, operator.methodcaller("droplevel", "A")),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("pop", "A")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("squeeze")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.Series, ([1, 2],), operator.methodcaller("squeeze")),
        # marks=not_implemented_mark,
    ),
    (pd.Series, ([1, 2],), operator.methodcaller("rename_axis", index="a")),
    (pd.DataFrame, frame_data, operator.methodcaller("rename_axis", columns="a")),
    # Unary ops
    (pd.DataFrame, frame_data, operator.neg),
    (pd.Series, [1], operator.neg),
    (pd.DataFrame, frame_data, operator.pos),
    (pd.Series, [1], operator.pos),
    (pd.DataFrame, frame_data, operator.inv),
    (pd.Series, [1], operator.inv),
    (pd.DataFrame, frame_data, abs),
    pytest.param((pd.Series, [1], abs), marks=not_implemented_mark),
    pytest.param((pd.DataFrame, frame_data, round), marks=not_implemented_mark),
    (pd.Series, [1], round),
    (pd.DataFrame, frame_data, operator.methodcaller("take", [0, 0])),
    (pd.DataFrame, frame_mi_data, operator.methodcaller("xs", "a")),
    (pd.Series, (1, mi), operator.methodcaller("xs", "a")),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("get", "A")),
        marks=not_implemented_mark,
    ),
    (
        pd.DataFrame,
        frame_data,
        operator.methodcaller("reindex_like", pd.DataFrame({"A": [1, 2, 3]})),
    ),
    (
        pd.Series,
        frame_data,
        operator.methodcaller("reindex_like", pd.Series([0, 1, 2])),
    ),
    (pd.DataFrame, frame_data, operator.methodcaller("add_prefix", "_")),
    (pd.DataFrame, frame_data, operator.methodcaller("add_suffix", "_")),
    (pd.Series, (1, ["a", "b"]), operator.methodcaller("add_prefix", "_")),
    (pd.Series, (1, ["a", "b"]), operator.methodcaller("add_suffix", "_")),
    (pd.Series, ([3, 2],), operator.methodcaller("sort_values")),
    (pd.Series, ([1] * 10,), operator.methodcaller("head")),
    (pd.DataFrame, ({"A": [1] * 10},), operator.methodcaller("head")),
    (pd.Series, ([1] * 10,), operator.methodcaller("tail")),
    (pd.DataFrame, ({"A": [1] * 10},), operator.methodcaller("tail")),
    (pd.Series, ([1, 2],), operator.methodcaller("sample", n=2, replace=True)),
    (pd.DataFrame, (frame_data,), operator.methodcaller("sample", n=2, replace=True)),
    (pd.Series, ([1, 2],), operator.methodcaller("astype", float)),
    (pd.DataFrame, frame_data, operator.methodcaller("astype", float)),
    (pd.Series, ([1, 2],), operator.methodcaller("copy")),
    (pd.DataFrame, frame_data, operator.methodcaller("copy")),
    (pd.Series, ([1, 2], None, object), operator.methodcaller("infer_objects")),
    (
        pd.DataFrame,
        ({"A": np.array([1, 2], dtype=object)},),
        operator.methodcaller("infer_objects"),
    ),
    (pd.Series, ([1, 2],), operator.methodcaller("convert_dtypes")),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("convert_dtypes")),
        marks=not_implemented_mark,
    ),
    (pd.Series, ([1, None, 3],), operator.methodcaller("interpolate")),
    (pd.DataFrame, ({"A": [1, None, 3]},), operator.methodcaller("interpolate")),
    (pd.Series, ([1, 2],), operator.methodcaller("clip", lower=1)),
    (pd.DataFrame, frame_data, operator.methodcaller("clip", lower=1)),
    (
        pd.Series,
        (1, pd.date_range("2000", periods=4)),
        operator.methodcaller("asfreq", "H"),
    ),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4)),
        operator.methodcaller("asfreq", "H"),
    ),
    (
        pd.Series,
        (1, pd.date_range("2000", periods=4)),
        operator.methodcaller("at_time", "12:00"),
    ),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4)),
        operator.methodcaller("at_time", "12:00"),
    ),
    (
        pd.Series,
        (1, pd.date_range("2000", periods=4)),
        operator.methodcaller("between_time", "12:00", "13:00"),
    ),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4)),
        operator.methodcaller("between_time", "12:00", "13:00"),
    ),
    (
        pd.Series,
        (1, pd.date_range("2000", periods=4)),
        operator.methodcaller("first", "3D"),
    ),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4)),
        operator.methodcaller("first", "3D"),
    ),
    (
        pd.Series,
        (1, pd.date_range("2000", periods=4)),
        operator.methodcaller("last", "3D"),
    ),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4)),
        operator.methodcaller("last", "3D"),
    ),
    (pd.Series, ([1, 2],), operator.methodcaller("rank")),
    (pd.DataFrame, frame_data, operator.methodcaller("rank")),
    (pd.Series, ([1, 2],), operator.methodcaller("where", np.array([True, False]))),
    (pd.DataFrame, frame_data, operator.methodcaller("where", np.array([[True]]))),
    (pd.Series, ([1, 2],), operator.methodcaller("mask", np.array([True, False]))),
    (pd.DataFrame, frame_data, operator.methodcaller("mask", np.array([[True]]))),
    (pd.Series, ([1, 2],), operator.methodcaller("slice_shift")),
    (pd.DataFrame, frame_data, operator.methodcaller("slice_shift")),
    (pd.Series, (1, pd.date_range("2000", periods=4)), operator.methodcaller("tshift")),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4)),
        operator.methodcaller("tshift"),
    ),
    (pd.Series, ([1, 2],), operator.methodcaller("truncate", before=0)),
    (pd.DataFrame, frame_data, operator.methodcaller("truncate", before=0)),
    (
        pd.Series,
        (1, pd.date_range("2000", periods=4, tz="UTC")),
        operator.methodcaller("tz_convert", "CET"),
    ),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4, tz="UTC")),
        operator.methodcaller("tz_convert", "CET"),
    ),
    (
        pd.Series,
        (1, pd.date_range("2000", periods=4)),
        operator.methodcaller("tz_localize", "CET"),
    ),
    (
        pd.DataFrame,
        ({"A": [1, 1, 1, 1]}, pd.date_range("2000", periods=4)),
        operator.methodcaller("tz_localize", "CET"),
    ),
    pytest.param(
        (pd.Series, ([1, 2],), operator.methodcaller("describe")),
        marks=not_implemented_mark,
    ),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("describe")),
        marks=not_implemented_mark,
    ),
    (pd.Series, ([1, 2],), operator.methodcaller("pct_change")),
    pytest.param(
        (pd.DataFrame, frame_data, operator.methodcaller("pct_change")),
        marks=not_implemented_mark,
    ),
]


def idfn(x):
    xpr = re.compile(r"'(.*)?'")
    m = xpr.search(str(x))
    if m:
        return m.group(1)
    else:
        return str(x)


@pytest.fixture(params=all_methods, ids=lambda x: idfn(x[-1]))
def ndframe_method(request):
    """
    An NDFrame method returning an NDFrame.
    """
    return request.param
