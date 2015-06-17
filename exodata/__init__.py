"""
Help?
"""
__version__ = '1.1.1.2.2'


def test():
    if sys.hexversion < 0x02070000:
        import unittest2 as unittest
    else:
        import unittest

    from tests import testsuite as _testsuite
    unittest.TextTestRunner(verbosity=2).run(_testsuite)

# OECPy Imports
import sys

# Import package modules
from . import assumptions, astroclasses, astroquantities, equations, example, flags, plots
# import OEC database
from .database import OECDatabase, load_db_from_url
