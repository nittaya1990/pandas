import pandas as pd

from pandas.io.json import dumps

dfexp = ('{"DT":{'
         '"0":"2013-01-01T05:00:00.000Z",'
         '"1":"2013-01-02T05:00:00.000Z"}}')


tz_range = pd.date_range('2013-01-01 05:00:00Z', periods=2)
dti = pd.DatetimeIndex(tz_range)
df = pd.DataFrame({'DT': dti})
result = dumps(df, iso_dates=True)
assert result == dfexp
