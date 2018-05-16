#!/usr/bin/env python
"""Create a blank whatsnew."""
import argparse
import sys

tpl = """\

.. _{link}:

{version}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _{link}.enhancements:

New features
~~~~~~~~~~~~

.. _{link}.enhancements.other:

Other Enhancements
^^^^^^^^^^^^^^^^^^
-
-
-

.. _{link}.api_breaking:


Backwards incompatible API changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _{link}.api.other:

Other API Changes
^^^^^^^^^^^^^^^^^

-
-
-

.. _{link}.deprecations:

Deprecations
~~~~~~~~~~~~

-
-
-

.. _{link}.prior_deprecations:

Removal of prior version deprecations/changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-
-
-

.. _{link}.performance:

Performance Improvements
~~~~~~~~~~~~~~~~~~~~~~~~

-
-
-

.. _{link}.docs:

Documentation Changes
~~~~~~~~~~~~~~~~~~~~~

-
-
-

.. _{link}.bug_fixes:

Bug Fixes
~~~~~~~~~

Categorical
^^^^^^^^^^^

-
-
-

Datetimelike
^^^^^^^^^^^^

-
-
-

Timedelta
^^^^^^^^^

-
-
-

Timezones
^^^^^^^^^

-
-
-

Offsets
^^^^^^^

-
-
-

Numeric
^^^^^^^

-
-
-

Strings
^^^^^^^

-
-
-

Indexing
^^^^^^^^

-
-
-

MultiIndex
^^^^^^^^^^

-
-
-

I/O
^^^

-
-
-

Plotting
^^^^^^^^

-
-
-

Groupby/Resample/Rolling
^^^^^^^^^^^^^^^^^^^^^^^^

-
-
-

Sparse
^^^^^^

-
-
-

Reshaping
^^^^^^^^^

-
-
-

Other
^^^^^

-
-
-
"""


def parse_args(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", type=str, help="Pandas version (0.23.0)")
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    link = "whatsnew_{}".format(args.version.replace(".", ""))

    version = 'v{}'.format(args.version)
    print(tpl.format(version=version, link=link))


if __name__ == '__main__':
    sys.exit(main())
