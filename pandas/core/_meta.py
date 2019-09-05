"""
Metadata propagation through pandas operations.

This module contains the infrastructure for propagating metadata
through operations. By metadata, we mean the attributes stored
in ``NDFrame._metadata``. We perform an operation
(say :meth:`pandas.Series.copy`) that returns an ``NDFrame``, and would
like to propagate the metadata (say ``Series.name``) from ``self`` to the
new ``NDFrame``.

Internally, pandas uses the :meth:`finalize` decorator to enable finalization.
In addition to performing the finalization before returning the result, :meth:`finalize`
creates a dictionary of which methods pandas finalizes. This is useful authors adding
custom metadata.
"""
from collections import defaultdict
from functools import partial, wraps
import inspect

from pandas.core.dtypes.generic import ABCDataFrame, ABCSeries

dispatch = defaultdict(dict)


def key_of(method):
    if isinstance(method, str):
        # TODO: figure out if this is OK. May be necessary when we have
        #   things like pd.merge and DataFrame.merge that hit the same finalize.
        return method
    elif method:
        return method.__module__, method.__name__


class PandasMetadata:
    """
    Dispatch metadata finalization for pandas metadata.

    Users should instantiate a single `PandasMetadata` instance
    for their piece of metadata and register finalizers for various
    pandas methods using :meth:`PandsaMetadata.register`.

    Parameters
    ----------
    name : str
        The name of the attribute being finalized.

    Examples
    --------
    >>> maxmeta = PandasMetadata("max_meta")
    >>> @maxmeta.register(pd.concat)
    ... def _(objs):
    ...     return max(x.max_meta for x in objs)
    """

    def __init__(self, name):
        self.name = name

    def register(self, pandas_method):
        """
        A decorator to register a finalizer for a specific pandas method.

        Parameters
        ----------
        pandas_method : Callable
            A pandas method, like :meth:`pandas.concat`, that this finalizer
            should be used for. The function being decorated should expect... what?
            When `NDFrame.__finalize__` is called as a result of `pandas_method`,
            the registered finalizer will be called.

        See Also
        --------
        default_finalizer
        """

        def decorate(func):
            # TODO: warn of collisions?
            dispatch[key_of(pandas_method)][self.name] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorate


def default_finalizer(new, other):
    """
    The default finalizer when this method, attribute hasn't been overridden.

    This copies the ``_metadata`` attributes from ``other`` to ``self``, modifying
    ``self`` inplace.

    Parameters
    ----------
    new : NDFrame
        The newly created NDFrame being finalized.
    other : NDFrame
        The source NDFrame attributes will be exracted from.
    """
    if isinstance(other, (ABCSeries, ABCDataFrame)):
        other = [other]

    for name in new._metadata:
        for o in other:
            if isinstance(o, (ABCSeries, ABCDataFrame)):
                object.__setattr__(new, name, getattr(o, name, None))


def finalize_all(new, other):

    assert len(new) == len(other)

    for n, o in zip(new, other):
        default_finalizer(n, o)


# ----------------------------------------------------------------------------
# Pandas Internals.
_METHODS = []
FINALIZERS = {}


def finalize(func=None, *, other=None, name=None):
    """
    Decorator to autom

    Parameters
    ----------
    func

    Examples
    --------
    >>> @finalize("objs")
    >>> def concat(objs, axis=0, ...):
    ...     ...

    This causes the output of ``concat`` to call ``NDFrame.__finalize__``
    with `to_concat` passed through as `other`.
    """
    if other is None:
        # allow use like @finalize to mean @finalize("self")
        return finalize(func=func, other="self")
        # return partial(finalize, other="self")
    if func is None:
        return partial(finalize, other=other)

    if name is None:
        # TODO: validate this...
        name = key_of(func)[1]
    _METHODS.append((name, other))
    FINALIZERS[name] = default_finalizer

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, (ABCSeries, ABCDataFrame)):
            other_value = get_other(func, other, args, kwargs)
            ndframe_finalize(result, other_value, func)
        return result

    print(f"wrapped {func} with {other}")
    return wrapper


def get_other(func, name, args, kwargs):
    # TODO: profile, maybe cache signature.
    sig = inspect.signature(func)
    bound = sig.bind(*args, **kwargs)
    if isinstance(name, str):
        name = [name]
    return [bound.arguments[n] for n in name]


def ndframe_finalize(new, other, method):
    """
    Finalize a new NDFrame.

    The finalizer is looked up from finalizers registered with PandasMetadata.

    Parameters
    ----------
    new : NDFrame
    other : NDFrame
        Or a list of them? TBD
    method : Callable

    Returns
    -------

    """
    for name in new._metadata:
        finalizer = dispatch.get(key_of(method), {}).get(name, default_finalizer)
        finalizer(new, other)
