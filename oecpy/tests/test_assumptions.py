import sys
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest


class Test_planetAssumptions(unittest.TestCase):

    def test_MassType(self):

        pass

if __name__ == '__main__':
    unittest.main()
