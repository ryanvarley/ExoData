import sys

if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest

testsuite = unittest.TestLoader().discover('.')