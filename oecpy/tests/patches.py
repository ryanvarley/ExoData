import sys
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest


class TestCase(unittest.TestCase):
    """ adds the assertItemsEqual back in python 3 by referencing assertCountEqual. This should by subclassed over
    unitest.Testcase by all test classes now
    """
    def assertItemsEqual(self, expected_seq, actual_seq, msg=None):
        if sys.hexversion < 0x03000000:
            return unittest.TestCase.assertItemsEqual(self, expected_seq, actual_seq, msg)
        else:
            return unittest.TestCase.assertCountEqual(self, expected_seq, actual_seq, msg)