import pytest
import numpy as np
import pandas as pd

from pandas.core.arrays.datetimetz import DatetimeTZArray
from pandas.core.dtypes.dtypes import DatetimeTZDtype
from pandas.tests.extension import base
from pandas.core.internals.blocks import DatetimeTZBlock


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




class BaseDatetimeTZTests(object):
    pass


class TestDtype(BaseDatetimeTZTests, base.BaseDtypeTests):
    pass


class TestConstructors(BaseDatetimeTZTests, base.BaseConstructorsTests):
    block = DatetimeTZBlock


class TestInterface(BaseDatetimeTZTests, base.BaseInterfaceTests):
    pass
