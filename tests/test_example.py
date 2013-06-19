import unittest

from exoplanetcatalogue.example import exampleSystem, exampleStar

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

if __name__ == '__main__':
    unittest.main()