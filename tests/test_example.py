""" These test check the example system is working correctly but also that paramters are formated correctly with the
right units.
"""
import unittest
import sys
from os.path import join
sys.path.append(join('..'))

from example import genExamplePlanet, examplePlanet

import astroquantities as aq
import quantities as pq

secondExamplePlanet = genExamplePlanet()


class TestExampleInstances(unittest.TestCase):

    def setUp(self):  # setup runs before each test!
        self.examplePlanet = examplePlanet
        self.exampleStar = self.examplePlanet.parent
        self.exampleSystem = self.exampleStar.parent

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

    def test_system_heirarchy(self):
        self.assertEqual(self.exampleSystem.stars[0], self.exampleStar)
        self.assertEqual(self.exampleStar.planets[0], self.examplePlanet)
        self.assertEqual(self.examplePlanet.parent, self.exampleStar)
        self.assertEqual(self.exampleStar.parent, self.exampleSystem)

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

if __name__ == '__main__':
    unittest.main()