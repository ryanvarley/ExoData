""" this includes code to check the params act globally over all modules as we expect, we don't really care about values
here. just that the calculation is performed.
"""
import unittest

import numpy as np

from .. import params
from .. import example as ex
from .. import astroquantities as aq
from .patches import TestCase


class estimateMissingValues(TestCase):

    def tearDown(self):
        """ reset back to default after
        """
        params.estimateMissingValues = True


class estimateMissingValuesPlanet(estimateMissingValues):

    def setUp(self):
        self.planet = ex.genExamplePlanet()

    def testSMAEstimatedWhenTrue(self):
        del self.planet.params['semimajoraxis']
        self.assertAlmostEqual(self.planet.a, 0.4496365 * aq.au, 7)
        self.assertTrue('Calculated SMA' in self.planet.flags.flags)

    def testSMANotEstimatedWhenFalse(self):
        params.estimateMissingValues = False
        del self.planet.params['semimajoraxis']
        self.assertTrue(self.planet.a is np.nan)
        self.assertTrue('Calculated SMA' not in self.planet.flags.flags)

    def testPeriodEstimatedWhenTrue(self):
        del self.planet.params['period']
        self.assertAlmostEqual(self.planet.P, 110.96397 * aq.day, 4)
        self.assertTrue('Calculated Period' in self.planet.flags.flags)

    def testPeriodNotEstimatedWhenFalse(self):
        params.estimateMissingValues = False
        del self.planet.params['period']
        self.assertTrue(self.planet.P is np.nan)
        self.assertTrue('Calculated Period' not in self.planet.flags.flags)

    def testTempEstimatedWhenTrue(self):
        del self.planet.params['temperature']
        self.assertAlmostEqual(self.planet.T, 402.175111 * aq.K, 4)
        self.assertTrue('Calculated Temperature' in self.planet.flags.flags)

    def testTempNotEstimatedWhenFalse(self):
        params.estimateMissingValues = False
        del self.planet.params['temperature']
        self.assertTrue(self.planet.T is np.nan)
        self.assertTrue('Calculated Temperature' not in self.planet.flags.flags)


class estimateMissingValuesStar(estimateMissingValues):

    def setUp(self):
        self.star = ex.genExampleStar()

    def test_magVEstimatedWhenTrue(self):
        del self.star.params['magV']
        self.assertAlmostEqual(self.star.magV, 9.14, 3)
        self.assertTrue('Estimated magV' in self.star.flags.flags)

    def test_magVNotEstimatedWhenFalse(self):
        params.estimateMissingValues = False
        del self.star.params['magV']
        self.assertTrue(self.star.magV is np.nan)
        self.assertTrue('Estimated magV' not in self.star.flags.flags)

    def testDistanceEstimatedWhenTrue(self):
        del self.star.system.params['distance']
        self.assertAlmostEqual(self.star.d, 60.256 * aq.pc, 3)
        self.assertTrue('Estimated Distance' in self.star.flags.flags)

    def testDistanceNotEstimatedWhenFalse(self):
        params.estimateMissingValues = False
        del self.star.system.params['distance']
        self.assertTrue(self.star.d is np.nan)
        self.assertTrue('Estimated Distance' not in self.star.flags.flags)


class estimateMissingValuesBinary(estimateMissingValues):

    def setUp(self):
        self.binary = ex.genExampleBinary()

    @unittest.skip('Currently the calculation is not implemented')
    def testSMAEstimatedWhenTrue(self):
        del self.binary.params['semimajoraxis']
        self.assertAlmostEqual(self.binary.a, 0.4496365 * aq.au, 7)
        self.assertTrue('Calculated SMA' in self.binary.flags.flags)

    def testSMANotEstimatedWhenFalse(self):
        params.estimateMissingValues = False
        del self.binary.params['semimajoraxis']
        self.assertTrue(self.binary.a is np.nan)
        self.assertTrue('Calculated SMA' not in self.binary.flags.flags)

    @unittest.skip('Currently the calculation is not implemented')
    def testPeriodEstimatedWhenTrue(self):
        del self.binary.params['period']
        self.assertAlmostEqual(self.binary.P, 110.96397 * aq.day, 4)
        self.assertTrue('Calculated Period' in self.binary.flags.flags)

    def testPeriodNotEstimatedWhenFalse(self):
        params.estimateMissingValues = False
        del self.binary.params['period']
        self.assertTrue(self.binary.P is np.nan)
        self.assertTrue('Calculated Period' not in self.binary.flags.flags)