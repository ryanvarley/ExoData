import sys
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

    def assertItemsAlmostEqual(self, expected_seq, actual_seq, places, msg=None):
        """ checks the length of both sequences and then each item is almost equal in turn. Order matters
        """
        self.assertEqual(len(expected_seq), len(actual_seq))

        for i, item in enumerate(expected_seq):
            self.assertAlmostEqual(item, actual_seq[i], places, msg)