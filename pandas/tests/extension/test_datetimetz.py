import pytest
import numpy as np
import pandas as pd

from pandas.core.arrays.datetimetz import DatetimeTZArray, to_datetimetz_array
from pandas.core.dtypes.dtypes import DatetimeTZDtype
from pandas.tests.extension import base


@pytest.fixture
def dtype():
    return DatetimeTZDtype(unit='ns', tz='US/Central')


@pytest.fixture
def data(dtype):
    # date_range('2017-01-01', periods=100, freq='D')
    values = np.arange(
        1483228800000000000, 1491868800000000000, 86400000000000
    ).view('datetime64[ns]')
    return DatetimeTZArray(values, dtype)


@pytest.fixture
def data_missing(dtype):
    return to_datetimetz_array(['NaT', '2017-01-01'], tz=dtype.tz)


@pytest.fixture
def na_value():
    return pd.NaT


class BaseDatetimeTZTests(object):
    pass


class TestDtype(BaseDatetimeTZTests, base.BaseDtypeTests):
    pass


class TestConstructors(BaseDatetimeTZTests, base.BaseConstructorsTests):
    pass


class TestInterface(BaseDatetimeTZTests, base.BaseInterfaceTests):

    def test_no_values_attribute(self, data):
        pass


class TestGetitem(BaseDatetimeTZTests, base.BaseGetitemTests):
    pass
