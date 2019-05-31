.. _best-practices:

Best Practices
--------------

This page describes ways of using pandas that we find easier to write, read, and maintain.
This style is lovingly referred to as *pandorable* code.

Throughout, we'll work with the tips dataset.

.. ipython:: python

   url = "https://raw.githubusercontent.com/pandas-dev/pandas/master/doc/data/tips.csv"
   df = pd.read_csv(url)

Do use Indexes
~~~~~~~~~~~~~~

One of pandas' defining features is its use of indexes for automatic alignment.
This can be thought of as the labeled version of NumPy's broadcasting.


