""" These test check the example system is working correctly but also that paramters are formated correctly with the
right units.
"""
import unittest

from exoplanetcatalogue.example import exampleSystem, exampleStar, examplePlanet

import exoplanetcatalogue.astroquantities as aq
import quantities as pq

class TestExampleInstances(unittest.TestCase):

    def test_system_object(self):
        self.assertEqual(exampleSystem.name, 'Example System')
        self.assertEqual(exampleSystem.d, 58 * pq.pc)
        self.assertEqual(exampleSystem.dec, '+04 05 06')
        self.assertEqual(exampleSystem.ra, '01 02 03')

    def test_star_object(self):
        self.assertEqual(exampleStar.params['altnames'], ['HD Example Star'])
        self.assertEqual(exampleStar.age, 7.6 * aq.Gyear)
        self.assertEqual(exampleStar.magB, 9.8)
        self.assertEqual(exampleStar.magH, 7.4)
        self.assertEqual(exampleStar.magI, 7.6)
        self.assertEqual(exampleStar.magJ, 7.5)
        self.assertEqual(exampleStar.magK, 7.3)
        self.assertEqual(exampleStar.magV, 9.0)
        self.assertEqual(exampleStar.M, 0.98 * aq.M_s)
        self.assertEqual(exampleStar.Z, 0.43)
        self.assertEqual(exampleStar.name, 'Example Star')
        self.assertEqual(exampleStar.R, 0.95 * aq.R_s)
        self.assertEqual(exampleStar.spectralType, 'G5')
        self.assertEqual(exampleStar.T, 5370 * pq.K)

    def test_planet_object(self):

        self.assertEqual(examplePlanet.discoveryMethod, 'transit')
        self.assertEqual(examplePlanet.discoveryYear, 2001)
        self.assertEqual(examplePlanet.e, 0.09)
        self.assertEqual(examplePlanet.i, 89.2 * pq.deg)
        self.assertEqual(examplePlanet.lastUpdate, '12/12/08')
        self.assertEqual(examplePlanet.M, 3.9 * aq.M_j)
        self.assertEqual(examplePlanet.name, 'Example Star b')
        self.assertEqual(examplePlanet.P, 111.2 * pq.d)
        self.assertEqual(examplePlanet.R, 0.92 * aq.R_j)
        self.assertEqual(examplePlanet.a, 0.449 * pq.au)
        self.assertEqual(examplePlanet.T, 339.6 * pq.K)
        self.assertEqual(examplePlanet.transittime, 2454876.344 * pq.d)

    def test_system_heirarchy(self):
        self.assertEqual(exampleSystem.stars[0], exampleStar)
        self.assertEqual(exampleStar.planets[0], examplePlanet)
        self.assertEqual(examplePlanet.parent, exampleStar)
        self.assertEqual(exampleStar.parent, exampleSystem)


if __name__ == '__main__':
    unittest.main()