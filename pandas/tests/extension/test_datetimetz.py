import pytest

from pandas.core.dtypes.dtypes import DatetimeTZDtype
from pandas.tests.extension import base


@pytest.fixture
def dtype():
    return DatetimeTZDtype(unit='ns', tz='US/Central')


class BaseDatetimeTZTests(object):
    pass


class TestDtype(base.BaseDtypeTests):
    pass