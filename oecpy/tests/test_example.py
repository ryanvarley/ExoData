""" These test check the example system is working correctly but also that paramters are formated correctly with the
right units.
"""
import sys
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest
import quantities as pq

from ..example import genExamplePlanet, examplePlanet, exampleSystem, exampleStar
from .. import astroquantities as aq
from .. import astroclasses as ac

secondExamplePlanet = genExamplePlanet()


class TestExampleInstances(unittest.TestCase):

    def setUp(self):  # setup runs before each test!
        ac._ExampleSystemCount = 1
        self.examplePlanet = examplePlanet
        self.exampleStar = exampleStar
        self.exampleSystem = exampleSystem

    def test_system_object(self):
        exampleSystem = self.exampleSystem

        self.assertEqual(exampleSystem.name, 'Example System 1')
        self.assertEqual(exampleSystem.d, 58 * pq.pc)
        self.assertEqual(exampleSystem.dec, '+04 05 06')
        self.assertEqual(exampleSystem.ra, '01 02 03')

    def test_star_object(self):
        exampleStar = self.exampleStar

        self.assertEqual(exampleStar.params['altnames'], ['HD 1'])
        self.assertEqual(exampleStar.age, 7.6 * aq.Gyear)
        self.assertEqual(exampleStar.magB, 9.8)
        self.assertEqual(exampleStar.magH, 7.4)
        self.assertEqual(exampleStar.magI, 7.6)
        self.assertEqual(exampleStar.magJ, 7.5)
        self.assertEqual(exampleStar.magK, 7.3)
        self.assertEqual(exampleStar.magV, 9.0)
        self.assertEqual(exampleStar.M, 0.98 * aq.M_s)
        self.assertEqual(exampleStar.Z, 0.43)
        self.assertEqual(exampleStar.name, 'Example Star 1')
        self.assertEqual(exampleStar.R, 0.95 * aq.R_s)
        self.assertEqual(exampleStar.spectralType, 'G5')
        self.assertEqual(exampleStar.T, 5370 * pq.K)
        self.assertEqual(exampleStar.getLimbdarkeningCoeff(1.22), (0.3531, 0.2822))

    def test_planet_object(self):
        examplePlanet = self.examplePlanet

        self.assertEqual(examplePlanet.discoveryMethod, 'transit')
        self.assertEqual(examplePlanet.discoveryYear, 2001)
        self.assertEqual(examplePlanet.e, 0.09)
        self.assertEqual(examplePlanet.i, 89.2 * pq.deg)
        self.assertEqual(examplePlanet.lastUpdate, '12/12/08')
        self.assertEqual(examplePlanet.M, 3.9 * aq.M_j)
        self.assertEqual(examplePlanet.name, 'Example Star 1 b')
        self.assertEqual(examplePlanet.P, 111.2 * pq.d)
        self.assertEqual(examplePlanet.R, 0.92 * aq.R_j)
        self.assertEqual(examplePlanet.a, 0.449 * pq.au)
        self.assertEqual(examplePlanet.T, 339.6 * pq.K)
        self.assertEqual(examplePlanet.transittime, 2454876.344 * pq.d)

    def test_hierarchy_for_planet(self):
        self.assertEqual(self.examplePlanet.star, self.exampleStar)
        self.assertEqual(self.examplePlanet.parent, self.exampleStar)
        self.assertEqual(self.examplePlanet.system, self.exampleSystem)

    def test_hierarchy_for_star(self):
        self.assertEqual(self.exampleStar.planets[0], self.examplePlanet)
        self.assertEqual(self.exampleStar.system, self.exampleSystem)
        self.assertEqual(self.exampleStar.parent, self.exampleSystem)

    def test_hierarchy_for_system(self):
        self.assertEqual(self.exampleSystem.stars[0], self.exampleStar)

    def test_raises_HeirarchyError_on_planet_binary_call_with_no_binary(self):
        with self.assertRaises(ac.HierarchyError):
            planetBinary = self.examplePlanet.binary

    def test_raises_HeirarchyError_on_star_binary_call_with_no_binary(self):
        with self.assertRaises(ac.HierarchyError):
            starBinary = self.exampleStar.binary

    def test_second_generation_is_number_2(self):
        examplePlanet = secondExamplePlanet
        exampleStar = examplePlanet.parent
        exampleSystem = exampleStar.parent

        self.assertEqual(examplePlanet.name, 'Example Star 2 b')
        self.assertEqual(exampleStar.name, 'Example Star 2')
        self.assertEqual(exampleStar.params['altnames'], ['HD 2'])
        self.assertEqual(exampleSystem.name, 'Example System 2')

    def test_second_generation_is_unique(self):

        planet1 = self.examplePlanet
        planet2 = secondExamplePlanet

        planet2.params['radius'] = 12345
        self.assertTrue(planet2.R, 12345)
        self.assertEqual(planet1.R, 0.92 * aq.R_j)


class TestExampleInstancesWithBinary(unittest.TestCase):

    def setUp(self):  # setup runs before each test!
        ac._ExampleSystemCount = 2
        self.examplePlanet = genExamplePlanet(binaryLetter='A')
        self.exampleStarA = self.examplePlanet.star
        self.exampleBinary = self.examplePlanet.binary
        self.exampleStarB = self.exampleBinary.stars[0]  # second star (without planet) - but it gets added first
        self.exampleSystem = self.examplePlanet.system

    def test_binary_object(self):
        exampleBinary = self.exampleBinary
        self.assertEqual(exampleBinary.name, 'Example Binary 2AB')  # already generated the example system 1 on import

    def test_hierarchy_for_planet(self):
        self.assertIsInstance(self.examplePlanet, ac.Planet)
        self.assertEqual(self.examplePlanet.name, 'Example Star 2A b')
        self.assertEqual(self.examplePlanet.system, self.exampleSystem)
        self.assertEqual(self.examplePlanet.star, self.exampleStarA)

    def test_hierarchy_for_starA(self):
        self.assertIsInstance(self.exampleStarA, ac.Star)
        self.assertEqual(self.exampleStarA.name, 'Example Star 2A')
        self.assertEqual(self.exampleStarA.system, self.exampleSystem)
        self.assertEqual(self.exampleStarA.planets[0], self.examplePlanet)

    def test_hierarchy_for_starB(self):
        self.assertIsInstance(self.exampleStarB, ac.Star)
        self.assertEqual(self.exampleStarB.name, 'Example Star 2B')
        self.assertEqual(self.exampleStarB.system, self.exampleSystem)
        self.assertFalse(self.exampleStarB.planets)

    def test_hierarchy_for_Binary(self):
        self.assertIsInstance(self.exampleBinary, ac.Binary)
        self.assertEqual(self.exampleBinary.name, 'Example Binary 2AB')
        self.assertEqual(self.exampleBinary.system, self.exampleSystem)
        self.assertItemsEqual(self.exampleBinary.stars, [self.exampleStarA, self.exampleStarB])

    def test_hierarchy_for_System(self):
        self.assertIsInstance(self.exampleSystem, ac.System)
        self.assertEqual(self.exampleSystem.name, 'Example System 2')
        self.assertItemsEqual(self.exampleSystem.stars, [self.exampleBinary])



if __name__ == '__main__':
    unittest.main()