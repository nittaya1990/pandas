import pandas as pd

from pandas.plotting._base import _backends, register_backend
from pandas.plotting._core import FramePlotMethods, SeriesPlotMethods


def test_register_backend():
    # define
    count = 0

    class MockedSeries(SeriesPlotMethods):
        def line(self, *args, **kwargs):
            nonlocal count
            count += 1
            super().line(*args, **kwargs)

    class MockedFrame(FramePlotMethods):
        def line(self, *args, **kwargs):
            nonlocal count
            count += 1
            super().line(*args, **kwargs)

    # register
    register_backend('mocked', MockedSeries, MockedFrame)
    assert 'mocked' in _backends

    # select
    pd.set_option("plotting.backend", "mocked")

    # use
    df = pd.DataFrame({"A": [1, 2], "B": [1, 2]})
    df.plot.line()
    assert count == 1
    df['A'].plot.line()
    assert count == 2
