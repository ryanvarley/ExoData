from .. import flags
from .patches import TestCase


class Test_Flag(TestCase):

    def test_flag__iter__(self):
        flagobj = flags.Flags()
        flagobj.addFlag('Calculated Temperature')
        flagobj.addFlag('Estimated Mass')

        self.assertTrue('Calculated Temperature' in flagobj)
        self.assertTrue('Estimated Mass' in flagobj)
        self.assertTrue('Calculated Period' not in flagobj)