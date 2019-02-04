from collections import namedtuple

PlottingBackend = namedtuple('PlottingBackend', 'series frame')

_backends = {}


def register_backend(name, series, frame):
    _backends[name] = PlottingBackend(series, frame)


class BasePlotMethods:
    def __init__(self, data):
        self._parent = data

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def area(self, *args, **kwargs):
        pass

    def bar(self, *args, **kwargs):
        pass

    def barh(self, *args, **kwargs):
        pass

    def box(self, *args, **kwargs):
        pass

    def density(self, *args, **kwargs):
        pass

    def hist(self, *args, **kwargs):
        pass

    def kde(self, *args, **kwargs):
        pass

    def line(self, *args, **kwargs):
        pass

    def pie(self, *args, **kwargs):
        pass


class SeriesPlotMethods(BasePlotMethods):
    def __call__(self, kind='line', ax=None,
                 figsize=None, use_index=True, title=None, grid=None,
                 legend=False, style=None, logx=False, logy=False,
                 loglog=False, xticks=None, yticks=None,
                 xlim=None, ylim=None,
                 rot=None, fontsize=None, colormap=None, table=False,
                 yerr=None, xerr=None,
                 label=None, secondary_y=False, **kwds):
        raise NotImplementedError


class FramePlotMethods(BasePlotMethods):

    def __call__(self, x=None, y=None, kind='line', ax=None,
                 subplots=False, sharex=None, sharey=False, layout=None,
                 figsize=None, use_index=True, title=None, grid=None,
                 legend=True, style=None, logx=False, logy=False, loglog=False,
                 xticks=None, yticks=None, xlim=None, ylim=None,
                 rot=None, fontsize=None, colormap=None, table=False,
                 yerr=None, xerr=None,
                 secondary_y=False, sort_columns=False, **kwds):
        pass

    def hexbin(self, x, y, **kwargs):
        pass

    def scatter(self, x, y, **kwargs):
        pass
