from pandas.core.arrays import ExtensionArray
from pandas.core.arrays.datetimelike import DatetimeLikeArrayMixin


class DatetimeTZArray(ExtensionArray, DatetimeLikeArrayMixin):
    """
    Pandas ExtensionArray for datetime data with timezone.

    This stores data as a NumPy array of datetime64[ns].
    The dtype consists of two fields, ``unit`` and ``tz``.
    """
    _attributes = ['dtype']

    def __init__(self, values, dtype):
        self._data = values
        self._dtype = dtype
        self.freq = None

    @classmethod
    def from_array(cls, values, tz):
        values = to_array(values)
        return cls(values, tz)

    @property
    def dtype(self):
        return self._dtype

    @property
    def tz(self):
        return self.dtype.tz

    # ------------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------------
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        pass

    def _from_factorized(cls, values, original):
        pass

    # ------------------------------------------------------------------------
    # Array
    # ------------------------------------------------------------------------
    def __len__(self):
        return len(self._data)

    @property
    def nbytes(self):
        return self._data.nbytes

    # ------------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------------

    def __getitem__(self, item):
        return self._data[item]


def to_array(values):
    return values
