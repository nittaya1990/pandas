import warnings

import numpy as np

from pandas.core.arrays import ExtensionArray
from pandas.core.arrays.datetimelike import DatetimeLikeArrayMixin
from pandas.core.dtypes.inference import (
    is_scalar,
)
from pandas.core.dtypes.dtypes import DatetimeTZDtype
from pandas._libs.tslib import Timestamp, NaT


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

    def __repr__(self):
        return "<DatetimeTZArray>({}, dtype={})".format(self.values, self.dtype)

    @classmethod
    def _simple_new(cls, values, **kwargs):
        return to_datetimetz_array(values, tz=kwargs.get('tz', None))

    @classmethod
    def from_array(cls, values, tz):
        values = to_datetimetz_array(values)
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
    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        # this is all changing
        npnat = np.datetime64('NaT')
        if dtype is None:
            for scalar in scalars:
                if getattr(scalar, 'tz', None):
                    # not na
                    dtype = DatetimeTZDtype('ns', scalar.tz)
                    break

        scalars = [npnat if val is NaT else val for val in scalars]
        return to_datetimetz_array(scalars, tz=dtype.tz)

    @classmethod
    def _from_factorized(cls, values, original):
        values = original.take(values)
        return cls(values, original.dtype)

    # ------------------------------------------------------------------------
    # Array
    # ------------------------------------------------------------------------
    def __len__(self):
        return len(self._data)

    @property
    def nbytes(self):
        return self._data.nbytes

    def isna(self):
        from pandas.core.missing import isna
        return isna(self._data)

    def copy(self, deep=False):
        return type(self)(self._data.copy(), dtype=self.dtype)

    # ------------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------------

    def __getitem__(self, item):
        if is_scalar(item):
            return Timestamp(self._data[item], tz=self.dtype.tz)
        return type(self)(self._data[item], dtype=self.dtype)

    def take(self, indices, allow_fill=False, fill_value=None):
        from pandas.core.algorithms import take
        if fill_value is None:
            fill_value = self.dtype.na_value

        result = take(self.values, indices,
                      allow_fill=allow_fill,
                      fill_value=fill_value)
        return type(self)(result, self.dtype)

    # ------------------------------------------------------------------------
    # Reshape
    # ------------------------------------------------------------------------
    @classmethod
    def _concat_same_type(cls, to_concat):
        assert len({x.dtype for x in to_concat}) == 1
        dtype = to_concat[0].dtype
        return cls(np.concatenate(to_concat), dtype=dtype)

    # ------------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------------
    def value_counts(self, dropna=True):
        from pandas.core.algorithms import value_counts

        if dropna:
            values = self[~self.isna()].values
        else:
            values = self.values

        # these are tz-naive
        counts = value_counts(values)
        return type(counts)(counts.values,
                            index=counts.index.astype(self.dtype),
                            name=counts.name,
                            copy=False)


def to_datetimetz_array(values, tz=None):
    with warnings.catch_warnings():
        # XXX: figure out how to infer / tz from values
        warnings.simplefilter("ignore", DeprecationWarning)
        values = np.asarray(values, dtype='datetime64[ns]')

    dtype = DatetimeTZDtype('ns', tz=tz)
    return DatetimeTZArray(values, dtype=dtype)
