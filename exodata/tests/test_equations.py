import sys
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest


import math

from .. import astroquantities as aq
from ..equations import scaleHeight, meanPlanetTemp, starLuminosity, ratioTerminatorToStar, SNRPlanet,\
    surfaceGravity, transitDuration, density, estimateMass, calcSemiMajorAxis, calcSemiMajorAxis2, calcPeriod, \
    estimateDistance, estimateAbsoluteMagnitude

from .. import equations as eq
from .patches import TestCase


class Test_scaleHeight(TestCase):
    def test_works_earth(self):

        mu_p = 28.964 * aq.u
        T_eff_p = 290 * aq.degK
        g_p = 9.81 * aq.m / aq.s ** 2

        answer = 8486.04 * aq.m
        result = scaleHeight(T_eff_p, mu_p, g_p)

        self.assertAlmostEqual(answer, result, 2)


class Test_meanPlanetTemp(TestCase):
    def test_works_mars(self):

        a = 1.524 * aq.au
        A_p = 0.25
        T_s = 5800 * aq.K
        R_s = 1 * aq.R_s

        answer = 231.1 * aq.K  # TODO actual answer 227.17
        result = meanPlanetTemp(A_p, T_s, R_s, a)

        self.assertAlmostEqual(answer, result, 1)


class Test_starLuminosity(TestCase):
    def test_works_sun(self):

        R_s = 1 * aq.R_s
        T_eff_s = 5780 * aq.degK

        answer = 3.89144e+26 * aq.W
        result = starLuminosity(R_s, T_eff_s)

        self.assertAlmostEqual(answer, result, delta=0.0001e27)


class Test_ratioTerminatorToStar(TestCase):
    def test_works_earth(self):

        H_p = 8500 * aq.m
        R_p = 1 * aq.R_e
        R_s = 1 * aq.R_s

        answer = 1.12264e-06 * aq.dimensionless
        result = ratioTerminatorToStar(H_p, R_p, R_s)

        self.assertTrue(answer - result < 0.001)


class Test_SNRPlanet(TestCase):
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


class Test_surfaceGravity(TestCase):
    def test_works_earth(self):

        R_p = 1 * aq.R_e
        M_p = 1 * aq.M_e

        answer = 9.823 * aq.m / aq.s**2
        result = surfaceGravity(M_p, R_p)

        self.assertAlmostEqual(answer, result, 2)


class Test_transitDuration(TestCase):
    def test_works_gj1214(self):

        R_p = 0.02 * aq.R_j
        R_s = 0.21 * aq.R_s
        i = 88.17 * aq.deg
        a = 0.014 * aq.au
        P = 1.58040482 * aq.day

        answer = 45.8329 * aq.min
        result = transitDuration(P, R_s, R_p, a, i)

        self.assertAlmostEqual(answer, result, 3)


class Test_logg(TestCase):
    def test_works_wasp10(self):
        """ Christian et al. 2009 values
        """
        answer = 4.51
        result = eq.logg(0.703*aq.M_s, 0.775*aq.R_s)

        self.assertAlmostEqual(answer, result, 1)


class Test_starTemperature(TestCase):

    def test_works_sun(self):
        answer = 5800 * aq.K
        result = eq.estimateStarTemperature(1*aq.M_s)

        self.assertAlmostEqual(answer, result, 0)

    def test_works_hd189(self):
        answer = 4939 * aq.K
        result = eq.estimateStarTemperature(0.846*aq.M_s)

        self.assertTrue(result-answer < 300)


class Test_transitDepth(TestCase):
    def test_works_gj1214(self):
        """Charbonneau et. al. 2009 values"""
        answer = 0.1162**2
        result = eq.transitDepth(0.2110*aq.R_s, 2.678*aq.R_e)
        self.assertAlmostEqual(answer, result, 3)


class Test_density(TestCase):
    def test_works_water(self):  # Doesnt work as its not a sphere

        M = 1 * aq.kg
        R = 1 * aq.m

        answer = 0.2387 * aq.kg / aq.m**3  # TODO calcluate this result manually
        result = density(M, R).rescale(aq.kg / aq.m**3)

        self.assertAlmostEqual(answer, result, 3)

    def test_works_hd189(self):

        M = 1.144 * aq.M_j
        R = 1.138 * aq.R_j

        answer = 1.0296 * aq.g / aq.cm**3  # real answer 0.963
        result = density(M, R)

        self.assertAlmostEqual(answer, result, 3)


class Test_estimateMass(TestCase):
    def test_works_jupiter(self):

        R = 6.9911 * (10**7) * aq.m
        d = 1.326 * aq.g / aq.cm**3

        result = estimateMass(R, d).rescale(aq.kg)
        answer = 1.898*(10**27)*aq.kg

        self.assertAlmostEqual(answer, result, delta=1e24)


@unittest.skip("Not written")
class Test_estimateStellarMass(TestCase):
    def test_works_gj1214(self):
        assert False


class Test_calcSemiMajorAxis(TestCase):
    def test_works_earth(self):

        M_s = aq.M_s
        P = 1 * aq.year

        result = calcSemiMajorAxis(P, M_s)
        answer = 1 * aq.au

        self.assertAlmostEqual(answer, result, 3)


class Test_calcSemiMajorAxis2(TestCase):
    def test_works_gj1214(self):

        T_p = 520 * aq.K
        T_s = 3026 * aq.K
        R_s = 0.21 * aq.R_s
        A_p = 0.3

        result = calcSemiMajorAxis2(T_p, T_s, A_p, R_s)
        answer = 0.01665 * aq.au

        self.assertAlmostEqual(answer, result, 3)


class Test_calcPeriod(TestCase):
    def test_works_gj1214(self):

        a = 0.014 * aq.au
        M_s = 0.153 * aq.M_s

        result = calcPeriod(a, M_s)
        answer = 1.546 * aq.day

        self.assertAlmostEqual(answer, result, 3)


class Test_impactParameter(TestCase):
    def test_works_wasp10b(self):
        """ Christian et al. 2009 values
        """
        result = eq.impactParameter(0.0369 * aq.au, 0.775 * aq.R_s, 86.9 * aq.deg)
        answer = 0.568
        self.assertAlmostEqual(result, answer, 1)  # error bars are 0.05/0.08


class Test_estimateDistance(TestCase):
    def test_works_online_example(self):

        m = 14
        M = 0

        result = estimateDistance(m, M, 0)
        answer = 6309.6 * aq.pc

        self.assertAlmostEqual(answer, result, 1)


class Test_createAbsMagEstimationDict(TestCase):

    def test_works(self):
        magTable, LClassRef = eq._createAbsMagEstimationDict()

        self.assertEqual(magTable['O'][8][LClassRef['V']], -4.9)
        self.assertEqual(magTable['A'][1][LClassRef['III']], 0.2)
        self.assertTrue(math.isnan(magTable['A'][7][LClassRef['Iab']]))


class Test_estimateAbsoluteMagnitude(TestCase):

    def test_works_no_interp(self):
        self.assertEqual(estimateAbsoluteMagnitude('O9'), -4.5)
        self.assertEqual(estimateAbsoluteMagnitude('B5'), -1.2)
        self.assertEqual(estimateAbsoluteMagnitude('A5'), 1.95)

    def test_works_no_classnum(self):
        self.assertEqual(estimateAbsoluteMagnitude('G'), 5.1)
        self.assertEqual(estimateAbsoluteMagnitude('A'), 1.95)

    def test_works_interp(self):
        self.assertEqual(estimateAbsoluteMagnitude('A6'), 2.075)
        self.assertEqual(estimateAbsoluteMagnitude('A0.5Iab'), -6.35)

    def test_nan_on_invalid_types(self):
        self.assertTrue(math.isnan(estimateAbsoluteMagnitude('L1')))

    def test_works_on_other_L_types(self):
        self.assertEqual(estimateAbsoluteMagnitude('O9V'), -4.5)
        self.assertEqual(estimateAbsoluteMagnitude('B5III'), -2.2)
        self.assertEqual(estimateAbsoluteMagnitude('F2Ia'), -8.0)


class Test_createMagConversionDict(TestCase):

    def test_works(self):
        magTable = eq._createMagConversionDict()

        self.assertEqual(magTable['A6'][10], '0.44')
        self.assertEqual(magTable['B0'][0], '30000')
        self.assertEqual(magTable['M6'][14], 'nan')

if __name__ == '__main__':
    unittest.main()