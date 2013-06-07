import unittest

import quantities as pq
import astroquantities as aq

from equations import scaleHeight, meanPlanetTemp, starLuminosity, ratioTerminatorToStar, SNRPlanet,\
    surfaceGravity, transitDuration


class Test_scaleHeight(unittest.TestCase):
    def test_works_earth(self):

        mu_p = 28.964 * pq.u
        T_eff_p = 290 * pq.degK
        g_p = 9.81 * pq.m / pq.s ** 2

        answer = 8486.04 * pq.m
        result = scaleHeight(T_eff_p, mu_p, g_p)

        self.assertAlmostEqual(answer, result, 2)


class Test_meanPlanetTemp(unittest.TestCase):
    def test_works_mars(self):

        a = 1.524 * pq.au
        A_p = 0.25
        T_s = 5800 * pq.K
        R_s = 1 * aq.R_s

        answer = 227.17 * pq.K
        result = meanPlanetTemp(A_p, T_s, R_s, a)

        self.assertAlmostEqual(answer, result, 2)


class Test_starLuminosity(unittest.TestCase):
    def test_works_sun(self):

        R_s = 1 * aq.R_s
        T_eff_s = 5780 * pq.degK

        answer = 3.891440112409585e+26 * pq.W
        result = starLuminosity(R_s, T_eff_s)

        self.assertEqual(answer, result)


class Test_ratioTerminatorToStar(unittest.TestCase):
    def test_works_earth(self):

        H_p = 8500 * pq.m
        R_p = 1 * aq.R_e
        R_s = 1 * aq.R_s

        answer = 1.12264e-06 * pq.dimensionless
        result = ratioTerminatorToStar(H_p, R_p, R_s)

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

        R_p = 1 * aq.R_e
        M_p = 1 * aq.M_e

        answer = 9.823 * pq.m / pq.s**2
        result = surfaceGravity(M_p, R_p)

        self.assertAlmostEqual(answer, result, 3)


class Test_transitDuration(unittest.TestCase):
    def test_works_gj1214(self):

        R_p = 0.02 * aq.R_j
        R_s = 0.21 * aq.R_s
        i = 88.17 * pq.deg
        a = 0.014 * pq.au
        P = 1.58040482 * pq.day

        answer = 45.8329 * pq.min
        result = transitDuration(P, R_s, R_p, a, i)

        self.assertAlmostEqual(answer, result, 3)


class Test_logg(unittest.TestCase):
    def test_works_gj1214(self):
        assert False


class Test_starTemperature(unittest.TestCase):
    def test_works_gj1214(self):
        assert False


class Test_transitDepth(unittest.TestCase):
    def test_works_gj1214(self):
        assert False


class Test_density(unittest.TestCase):
    def test_works_gj1214(self):
        assert False


class Test_estimateMass(unittest.TestCase):
    def test_works_gj1214(self):
        assert False

if __name__ == '__main__':
    unittest.main()