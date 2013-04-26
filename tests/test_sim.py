import unittest

import quantities as pq

from ease.tools.sim import scaleHeight, meanPlanetTemp, starLuminosity, ratioTerminatorToStar, SNRPlanet,\
    surfaceGravity, transitDuration


class Test_scaleHeight(unittest.TestCase):
    def test_works_earth(self):
        params = {
            'mu_p': 28.964 * pq.u,
            'T_eff_p': 290 * pq.degK,
            'g_p': 9.81 * pq.m / pq.s ** 2,
        }

        answer = 8486.04 * pq.m
        result = scaleHeight(params)

        self.assertAlmostEqual(answer, result, 2)


class Test_meanPlanetTemp(unittest.TestCase):
    def test_works_mars(self):
        params = {
            'a': 1.524 * pq.au,
            'L_s': 3.844e26 * pq.W,
            'A_p': 0.25,
        }

        answer = 210.03 * pq.K
        result = meanPlanetTemp(params)

        self.assertAlmostEqual(answer, result, 2)


class Test_starLuminosity(unittest.TestCase):
    def test_works_sun(self):
        params = {
            'R_s': 1 * pq.R_s,
            'T_eff_s': 5780 * pq.degK
        }

        answer = 3.891440112409585e+26 * pq.W
        result = starLuminosity(params)

        self.assertEqual(answer, result)


class Test_ratioTerminatorToStar(unittest.TestCase):
    def test_works_earth(self):
        params = {'H_p': 8500 * pq.m,
                  'R_p': 1 * pq.R_e,
                  'R_s': 1 * pq.R_s
        }

        answer = 1.12264e-06 * pq.dimensionless
        result = ratioTerminatorToStar(params)

        self.assertTrue(answer - result < 0.001)


class Test_SNRPlanet(unittest.TestCase):
    def test_works(self):

        params = {'SNRStar': 400,
                  'starPlanetFlux': 1.12e-06,
                  'Nobs': 200,
                  'pixPerbin': 5,
                  'NVisits': 1,
                  }

        answer = 0.01417
        result = SNRPlanet(**params)

        self.assertAlmostEqual(answer, result, 5)


class Test_surfaceGravity(unittest.TestCase):
    def test_works_earth(self):

        params = {'R_p': 1 * pq.R_e,
                  'M_p': 1 * pq.M_e,
                  }

        answer = 9.823 * pq.m / pq.s**2
        result = surfaceGravity(params)

        self.assertAlmostEqual(answer, result, 3)


class Test_transitDuration(unittest.TestCase):
    def test_works_gj1214(self):

        params = {
            'R_p': 0.02 * pq.R_j,
            'R_s': 0.21 * pq.R_s,
            'i': 88.17 * pq.deg,
            'a': 0.014 * pq.au,
            'P': 1.58040482 * pq.day
        }

        answer = 45.8329 * pq.min
        result = transitDuration(params)

        self.assertAlmostEqual(answer, result, 3)


if __name__ == '__main__':
    unittest.main()