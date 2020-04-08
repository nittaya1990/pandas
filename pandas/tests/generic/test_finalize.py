"""
An exhaustive list of pandas methods exercising NDFrame.__finalize__.
"""
import operator

import pytest

import pandas as pd

from .conftest import idfn, not_implemented_mark

# TODO:
# * Binary methods (mul, div, etc.)
# * Binary outputs (align, etc.)
# * transform, apply
# * top-level methods (concat, merge, get_dummies, etc.)
# * groupby
# * window
# * cumulative reductions


def test_finalize_called(ndframe_method):
    cls, init_args, method = ndframe_method
    ndframe = cls(*init_args)

    ndframe.attrs = {"a": 1}
    result = method(ndframe)

    assert result.attrs == {"a": 1}


# ----------------------------------------------------------------------------
# Accessors


@pytest.mark.parametrize(
    "method",
    [
        operator.methodcaller("capitalize"),
        operator.methodcaller("casefold"),
        pytest.param(
            operator.methodcaller("cat", ["a"]),
            marks=pytest.mark.xfail(reason="finalize not called."),
        ),
        operator.methodcaller("contains", "a"),
        operator.methodcaller("count", "a"),
        operator.methodcaller("encode", "utf-8"),
        operator.methodcaller("endswith", "a"),
        pytest.param(
            operator.methodcaller("extract", r"(\w)(\d)"),
            marks=pytest.mark.xfail(reason="finalize not called."),
        ),
        pytest.param(
            operator.methodcaller("extract", r"(\w)(\d)"),
            marks=pytest.mark.xfail(reason="finalize not called."),
        ),
        operator.methodcaller("find", "a"),
        operator.methodcaller("findall", "a"),
        operator.methodcaller("get", 0),
        operator.methodcaller("index", "a"),
        operator.methodcaller("len"),
        operator.methodcaller("ljust", 4),
        operator.methodcaller("lower"),
        operator.methodcaller("lstrip"),
        operator.methodcaller("match", r"\w"),
        operator.methodcaller("normalize", "NFC"),
        operator.methodcaller("pad", 4),
        operator.methodcaller("partition", "a"),
        operator.methodcaller("repeat", 2),
        operator.methodcaller("replace", "a", "b"),
        operator.methodcaller("rfind", "a"),
        operator.methodcaller("rindex", "a"),
        operator.methodcaller("rjust", 4),
        operator.methodcaller("rpartition", "a"),
        operator.methodcaller("rstrip"),
        operator.methodcaller("slice", 4),
        operator.methodcaller("slice_replace", 1, repl="a"),
        operator.methodcaller("startswith", "a"),
        operator.methodcaller("strip"),
        operator.methodcaller("swapcase"),
        operator.methodcaller("translate", {"a": "b"}),
        operator.methodcaller("upper"),
        operator.methodcaller("wrap", 4),
        operator.methodcaller("zfill", 4),
        operator.methodcaller("isalnum"),
        operator.methodcaller("isalpha"),
        operator.methodcaller("isdigit"),
        operator.methodcaller("isspace"),
        operator.methodcaller("islower"),
        operator.methodcaller("isupper"),
        operator.methodcaller("istitle"),
        operator.methodcaller("isnumeric"),
        operator.methodcaller("isdecimal"),
        operator.methodcaller("get_dummies"),
    ],
    ids=idfn,
)
@not_implemented_mark
def test_string_method(method):
    s = pd.Series(["a1"])
    s.attrs = {"a": 1}
    result = method(s.str)
    assert result.attrs == {"a": 1}


@pytest.mark.parametrize(
    "method",
    [
        operator.methodcaller("to_period"),
        operator.methodcaller("tz_localize", "CET"),
        operator.methodcaller("normalize"),
        operator.methodcaller("strftime", "%Y"),
        operator.methodcaller("round", "H"),
        operator.methodcaller("floor", "H"),
        operator.methodcaller("ceil", "H"),
        operator.methodcaller("month_name"),
        operator.methodcaller("day_name"),
    ],
    ids=idfn,
)
@not_implemented_mark
def test_datetime_method(method):
    s = pd.Series(pd.date_range("2000", periods=4))
    s.attrs = {"a": 1}
    result = method(s.dt)
    assert result.attrs == {"a": 1}


@pytest.mark.parametrize(
    "attr",
    [
        "date",
        "time",
        "timetz",
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
        "nanosecond",
        "week",
        "weekofyear",
        "dayofweek",
        "dayofyear",
        "quarter",
        "is_month_start",
        "is_month_end",
        "is_quarter_start",
        "is_quarter_end",
        "is_year_start",
        "is_year_end",
        "is_leap_year",
        "daysinmonth",
        "days_in_month",
    ],
)
@not_implemented_mark
def test_datetime_property(attr):
    s = pd.Series(pd.date_range("2000", periods=4))
    s.attrs = {"a": 1}
    result = getattr(s.dt, attr)
    assert result.attrs == {"a": 1}


@pytest.mark.parametrize(
    "attr", ["days", "seconds", "microseconds", "nanoseconds", "components"]
)
@not_implemented_mark
def test_timedelta_property(attr):
    s = pd.Series(pd.timedelta_range("2000", periods=4))
    s.attrs = {"a": 1}
    result = getattr(s.dt, attr)
    assert result.attrs == {"a": 1}


@pytest.mark.parametrize(
    "method", [operator.methodcaller("total_seconds")],
)
@not_implemented_mark
def test_timedelta_methods(method):
    s = pd.Series(pd.timedelta_range("2000", periods=4))
    s.attrs = {"a": 1}
    result = method(s.dt)
    assert result.attrs == {"a": 1}
