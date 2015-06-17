import unittest

import math

from hypothesis import given, example, assume, Settings, Verbosity
from hypothesis.strategies import floats

from .. import astroquantities as aq
from ..equations import ScaleHeight, MeanPlanetTemp, StellarLuminosity, ratioTerminatorToStar, SNRPlanet,\
    surfaceGravity, transitDuration, density, estimateMass, calcSemiMajorAxis, calcSemiMajorAxis2, KeplersThirdLaw, \
    estimateDistance, estimateAbsoluteMagnitude, ExoDataEqn

from .. import equations as eq
from .patches import TestCase

Settings.default.verbosity = Verbosity.verbose

class Test_ExoDataEqn(TestCase):

    def test__repr__(self):

        eqn = ExoDataEqn()

        self.assertEqual(eqn.__repr__(), 'ExoDataEqn()')


class Test_ScaleHeight(TestCase):

    def test__repr__works(self):

        eqn = ScaleHeight(100*aq.K, 1*aq.atomic_mass_unit, 9.81 * aq.m / aq.s ** 2)

        answer = 'ScaleHeight(H=None, T_eff=100.0 K, mu=1.0 u, g=9.81 m/s**2)'

        self.assertEqual(eqn.__repr__(), answer)

    def test_works_earth(self):

        mu_p = 28.964 * aq.u
        T_eff_p = 290 * aq.degK
        g_p = 9.81 * aq.m / aq.s ** 2

        answer = 8486.04 * aq.m
        result = ScaleHeight(T_eff_p, mu_p, g_p).H

        self.assertAlmostEqual(answer, result, 2)

    @given(floats(0,), floats(0,), floats(0,))
    def test_can_derive_other_vars_from_one_calculated(self, T_eff, mu, g):
        """ We calculate H from a range of values given by hypothesis and then see if we can accurately calculate the
         other variables given this calculated value. This tests the rearrangements of the equation are correct.
        :return:
        """
        assume(T_eff > 0 and mu > 0 and g > 0)
        inf = float('inf')
        assume(T_eff < inf and mu < inf and g < inf)

        T_eff *= aq.K
        mu *= aq.atomic_mass_unit
        g *= aq.m / aq.s ** 2

        H = ScaleHeight(T_eff, mu, g, None).H

        self.assertAlmostEqual(ScaleHeight(T_eff, mu, None, H).g, g, 4)
        self.assertAlmostEqual(ScaleHeight(T_eff, None, g, H).mu, mu, 4)
        self.assertAlmostEqual(ScaleHeight(None, mu, g, H).T_eff, T_eff, 4)


class Test_MeanPlanetTemp(TestCase):
    def test_works_mars(self):

        a = 1.524 * aq.au
        A = 0.25
        T_s = 5800 * aq.K
        R_s = 1 * aq.R_s

        answer = 231.1 * aq.K  # TODO actual answer 227.17
        result = MeanPlanetTemp(A, T_s, R_s, a, 0.7).T_p

        self.assertAlmostEqual(answer, result, 1)

    @given(A=floats(0.0001, 1), T_s=floats(0.0001,), R_s=floats(0.001,), a=floats(0.0001,), epsilon=floats(0.0001, 1))
    def test_can_derive_other_vars_from_one_calculated(self, A, T_s, R_s, a, epsilon):
        assume(T_s > 0 and R_s > 0 and a > 0 and epsilon > 0)
        inf = float('inf')
        assume(T_s < inf and R_s < inf and a < inf)

        T_s *= aq.K
        R_s *= aq.R_s
        a *= aq.au

        T_p = MeanPlanetTemp(A, T_s, R_s, a, epsilon).T_p

        self.assertAlmostEqual(MeanPlanetTemp(A, T_s, R_s, a, None, T_p).epsilon, epsilon, 4)
        self.assertAlmostEqual(MeanPlanetTemp(A, T_s, R_s, None, epsilon, T_p).a, a, 4)
        self.assertAlmostEqual(MeanPlanetTemp(A, T_s, None, a, epsilon, T_p).R_s, R_s, 4)
        self.assertAlmostEqual(MeanPlanetTemp(A, None, R_s, a, epsilon, T_p).T_s, T_s, 4)
        self.assertAlmostEqual(MeanPlanetTemp(None, T_s, R_s, a, epsilon, T_p).A, A, 4)


class Test_StellarLuminosity(TestCase):
    def test_works_sun(self):

        R_s = 1 * aq.R_s
        T_eff_s = 5780 * aq.degK

        answer = 3.89144e+26 * aq.W
        result = StellarLuminosity(R_s, T_eff_s).L

        self.assertAlmostEqual(answer, result, delta=0.0001e27)

    @given(T=floats(0.0001), R=floats(0.0001))
    def test_can_derive_other_vars_from_one_calculated(self, T, R):
        assume(T > 0 and R > 0)
        inf = float('inf')
        assume(T < inf and R < inf)

        T *= aq.K
        R *= aq.R_s

        L = StellarLuminosity(R, T).L

        self.assertAlmostEqual(StellarLuminosity(R, None, L).T, T, 4)
        self.assertAlmostEqual(StellarLuminosity(None, T, L).R, R, 4)


class Test_KeplersThirdLaw(TestCase):

    def test_works_gj1214(self):

        a = 0.014 * aq.au
        M_s = 0.153 * aq.M_s

        result = KeplersThirdLaw(a, M_s).P
        answer = 1.546 * aq.day

        self.assertAlmostEqual(answer, result, 3)

    @given(a=floats(0.0001), M_s=floats(0.0001), M_p=floats(0,))
    def test_can_derive_other_vars_from_one_calculated(self, a, M_s, M_p):
        assume(M_s > 0 and a > 0)
        inf = float('inf')
        assume(a < inf and M_s < inf and M_p < inf)

        a *= aq.au
        M_s *= aq.M_s
        M_p *= aq.M_j

        P = KeplersThirdLaw(a, M_s, None, M_p).P

        self.assertAlmostEqual(KeplersThirdLaw(None, M_s, P, M_p).a, a, 4)
        self.assertAlmostEqual(KeplersThirdLaw(a, None, P, M_p).M_s, M_s, 4)
        self.assertAlmostEqual(KeplersThirdLaw(a, M_s, P, None).M_p, M_p, 4)


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