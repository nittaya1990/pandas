"""
Utilities for implementing 2D compatibility for 1D ExtensionArrays.
"""
from typing import Tuple

import numpy as np

from pandas._libs.lib import is_integer


def slice_contains_zero(slc: slice) -> bool:
    if slc == slice(None):
        return True
    if slc == slice(0, None):
        return True
    if slc == slice(0, 1):
        return True
    if slc.start == slc.stop:
        # Note: order matters here, since we _dont_ want this to catch
        #  the slice(None) case.
        return False
    raise NotImplementedError(slc)


def expand_key(key, shape):
    ndim = len(shape)
    if ndim != 2 or shape[0] != 1:
        raise NotImplementedError
    if not isinstance(key, tuple):
        key = (key, slice(None))
    if len(key) != 2:
        raise ValueError(key)

    if is_integer(key[0]) and key[0] not in [0, -1]:
        raise ValueError(key)

    return key


def can_safe_ravel(shape: Tuple[int, ...]) -> bool:
    """
    Check if an array with the given shape can be ravelled unambiguously
    regardless of column/row order.

    Parameters
    ----------
    shape : tuple[int]

    Returns
    -------
    bool
    """
    if len(shape) == 1:
        return True
    if len(shape) > 2:
        raise NotImplementedError(shape)
    if shape[0] == 1 or shape[1] == 1:
        # column-like or row-like
        return True
    return False


def tuplify_shape(size: int, shape, restrict=True) -> Tuple[int, ...]:
    """
    Convert a passed shape into a valid tuple.
    Following ndarray.reshape, we accept either `reshape(a, b)` or
    `reshape((a, b))`, the latter being canonical.

    Parameters
    ----------
    size : int
    shape : tuple
    restrict : bool, default True
        Whether to restrict to shapes (N), (1,N), and (N,1)

    Returns
    -------
    tuple[int, ...]
    """
    if len(shape) == 0:
        raise ValueError("shape must be a non-empty tuple of integers", shape)

    if len(shape) == 1:
        if is_integer(shape[0]):
            pass
        else:
            shape = shape[0]
            if not isinstance(shape, tuple):
                raise ValueError("shape must be a non-empty tuple of integers", shape)

    if not all(is_integer(x) for x in shape):
        raise ValueError("shape must be a non-empty tuple of integers", shape)

    if any(x < -1 for x in shape):
        raise ValueError("Invalid shape {shape}".format(shape=shape))

    if -1 in shape:
        if shape.count(-1) != 1:
            raise ValueError("Invalid shape {shape}".format(shape=shape))
        idx = shape.index(-1)
        others = [n for n in shape if n != -1]
        prod = np.prod(others)
        dim = size // prod
        shape = shape[:idx] + (dim,) + shape[idx + 1 :]

    if np.prod(shape) != size:
        raise ValueError(
            "Product of shape ({shape}) must match "
            "size ({size})".format(shape=shape, size=size)
        )

    num_gt1 = len([x for x in shape if x > 1])
    if num_gt1 > 1 and restrict:
        raise ValueError(
            "The default `reshape` implementation is limited to "
            "shapes (N,), (N,1), and (1,N), not {shape}".format(shape=shape)
        )
    return shape
