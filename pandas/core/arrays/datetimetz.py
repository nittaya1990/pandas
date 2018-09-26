from pandas.core.arrays import ExtensionArray
from pandas.core.arrays.datetimelike import DatetimeLikeArrayMixin


class DatetimeTZArray(ExtensionArray, DatetimeLikeArrayMixin):
    pass