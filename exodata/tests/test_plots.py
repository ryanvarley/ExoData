import unittest

from .patches import TestCase

import numpy as np


from ..example import genExamplePlanet
from ..plots import DataPerParameterBin, GeneralPlotter, _AstroObjectFigs, _GlobalFigure, _planetPars, _starPars
from .. import astroquantities as aq


class Test_GlobalFigure(TestCase):

    def test_set_y_axis_log(self):  # Simple test to ensure theres no exception
        fig = _GlobalFigure()
        fig.set_y_axis_log()

    def test_set_x_axis_log(self):
        fig = _GlobalFigure()
        fig.set_x_axis_log()


class Test_AstroObjectFigs(TestCase):

    @unittest.skip("Tested through others but should probably be done here aswell")
    def test_getInputObjectTypes(self):
        assert False

    @unittest.skip("Tested through others but should probably be done here aswell")
    def test_getParLabelAndUnit(self):
        assert False

    def test_gen_label(self):
        fig = _AstroObjectFigs([genExamplePlanet()])
        self.assertEqual(fig._gen_label('R', None), 'Planet Radius')
        self.assertEqual(fig._gen_label('R', aq.m), 'Planet Radius (m)')
        self.assertEqual(fig._gen_label('R', aq.R_j), 'Planet Radius ($R_J$)')

    def test_get_unit_symbol(self):
        fig = _AstroObjectFigs([genExamplePlanet()])
        self.assertEqual(fig._get_unit_symbol(aq.m), 'm')
        self.assertEqual(fig._get_unit_symbol(aq.R_j), '$R_J$')

    def test_get_unit_symbol_with_no_unit_raises_error(self):
        fig = _AstroObjectFigs([genExamplePlanet()])
        with self.assertRaises(AttributeError):
            fig._get_unit_symbol(None)


class Test_DataPerParameterBin(TestCase):

    def testDataGeneratesCorrectly(self):
        planets = []
        planetInfoList = (0, 0.1, 0.2, 0.3, 0.45, 0.5, 0.6, np.nan)

        for planetInfo in planetInfoList:
            planet = genExamplePlanet()
            planet.params['eccentricity'] = planetInfo
            planets.append(planet)

        data = DataPerParameterBin(planets, 'e', (0, 0.2, 0.4, 0.6))
        answer = {'0 to 0.2': 2, '0.2 to 0.4': 2, '0.4 to 0.6': 3, 'Uncertain': 1}

        self.assertDictEqual(answer, data._processResults())

    def test_limits_generated_correctly(self):
        planets = []
        planetInfoList = (-10, -4, -1, 1, 3, 5, 6, 7, 8 , np.nan)

        for planetInfo in planetInfoList:
            planet = genExamplePlanet()
            planet.params['eccentricity'] = planetInfo
            planets.append(planet)

        data = DataPerParameterBin(planets, 'e', (-float('inf'), 0, 5, float('inf')))

        answer = {'<0': 3, '0 to 5': 2, '5+': 4, 'Uncertain': 1}
        self.assertDictEqual(answer, data._processResults())

    def testDataGeneratesCorrectlyWithUnitScaling(self):
        planets = []
        planetInfoList = (0*aq.R_j, 0.1*aq.R_j, 0.2*aq.R_j, 0.3*aq.R_j, 0.45*aq.R_j, 0.5*aq.R_j, 0.6*aq.R_j, np.nan)

        for planetInfo in planetInfoList:
            planet = genExamplePlanet()
            planet.params['radius'] = planetInfo
            planets.append(planet)

        data = DataPerParameterBin(planets, 'R', (0, 5, 15, 30), aq.R_e)
        answer = {'0 to 5': 5, '5 to 15': 2, '15 to 30': 0, 'Uncertain': 1}

        self.assertDictEqual(answer, data._processResults())

    def testStarRadiusGeneratesCorrectly(self):
        starInfoList = (0*aq.R_s, 1*aq.R_s, 2*aq.R_s, 3*aq.R_s, 4.5*aq.R_s, 5*aq.R_s, 6*aq.R_s, np.nan)
        planets = generate_list_of_planets(len(starInfoList))
        starlist = [planet.star for planet in planets]

        for i, star in enumerate(starlist):
            star.params['radius'] = starInfoList[i]

        data = DataPerParameterBin(starlist, 'R', (0, 5, 15, 30), aq.R_s)
        answer = {'0 to 5': 5, '5 to 15': 2, '15 to 30': 0, 'Uncertain': 1}

        self.assertDictEqual(answer, data._processResults())

    def test_plotbarchart_for_all_planet_params_generate_without_exception(self):
        planetlist = generate_list_of_planets(3)

        for param in _planetPars:
            DataPerParameterBin(planetlist, param, (-float('inf'), 0, 5, float('inf'))).plotBarChart()

    def test_plotbarchart_for_all_stellar_params_generate_without_exception(self):
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]

        for param in _starPars:
            DataPerParameterBin(starlist, param, (-float('inf'), 0, 5, float('inf'))).plotBarChart()

    def test_plotbarchart_for_all_planet_and_star_classes_on_input_raises_TypeError(self):
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]

        with self.assertRaises(TypeError):
            fig = DataPerParameterBin(starlist + planetlist, 'R', (-float('inf'), 0, 5, float('inf'))).plotBarChart()

    def test_plotpiechart_for_all_planet_params_generate_without_exception(self):
        planetlist = generate_list_of_planets(3)

        for param in _planetPars:
            DataPerParameterBin(planetlist, param, (-float('inf'), 0, 5, float('inf'))).plotPieChart()

    def test_plotpiechart_for_all_stellar_params_generate_without_exception(self):
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]

        for param in _starPars:
            DataPerParameterBin(starlist, param, (-float('inf'), 0, 5, float('inf'))).plotPieChart()


def generate_list_of_planets(number):
    planetList = []
    for i in range(number):
        planetList.append(genExamplePlanet())
    return planetList


class Test_GeneralPlotter(TestCase):

    def test__init__(self):
        x = GeneralPlotter(generate_list_of_planets(3))

    def test_set_axis_with_variables(self):
        planetlist = generate_list_of_planets(3)
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius

        fig = GeneralPlotter(planetlist)
        self.assertItemsEqual(fig._set_axis('R', None), radiusValues)

    def test_set_axis_with_variables_star(self):  # more of a test that it can correctly switch between planets and stars
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]
        radiusValues = (5*aq.R_s, 10*aq.R_s, 15*aq.R_s)

        for i, radius in enumerate(radiusValues):
            starlist[i].params['radius'] = radius

        fig = GeneralPlotter(starlist)
        self.assertItemsEqual(fig._set_axis('R', None), radiusValues)

    def test_set_axis_with_variables_planet_and_star(self):  # more of a test that it can correctly switch between planets and stars
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)
        magVValues = (1, 2, 3)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius
            starlist[i].params['magV'] = magVValues[i]

        fig = GeneralPlotter(planetlist)
        fig.set_xaxis('R', None)
        fig.set_yaxis('star.magV', None)
        self.assertItemsAlmostEqual(fig._xaxis, radiusValues, 1)
        self.assertItemsAlmostEqual(fig._yaxis, magVValues, 1)
        fig.plot()

    def test_set_axis_with_functions(self):
        planetlist = generate_list_of_planets(3)
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius

        fig = GeneralPlotter(planetlist)
        results = fig._set_axis('calcDensity()', None)
        answer = (0.04138 * aq.g/aq.cm**3, 0.00517 * aq.g/aq.cm**3, 0.00153 * aq.g/aq.cm**3)

        self.assertItemsAlmostEqual(answer, results, 4)

    def test_set_axis_with_unit_scaling(self):
        planetlist = generate_list_of_planets(3)
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius

        fig = GeneralPlotter(planetlist)
        # for some reason the items equal assert fails, comparing the str representations is equivilent with strict order
        self.assertItemsAlmostEqual(fig._set_axis('R', aq.m), [x.rescale(aq.m) for x in radiusValues], 4)

    def test_set_axis_with_unitless_stellar_quantity(self):
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]
        magVValues = (5, 10, 15)

        for i, magV in enumerate(magVValues):
            starlist[i].params['magV'] = magV

        fig = GeneralPlotter(starlist)
        # for some reason the items equal assert fails, comparing the str representations is equivilent with strict order
        self.assertItemsEqual(fig._set_axis('magV', None), magVValues)

    def test_plotting_on_all_planet_params_generate_without_exception(self):
        planetlist = generate_list_of_planets(3)

        for param in _planetPars:
            # print(param, [eval('planet.'+param) for planet in planetlist])
            # we are not testing the result, just that no exceptions are raised
            fig = GeneralPlotter(planetlist, param, 'R').plot()  # need X and Y to plot correctly

    def test_plotting_on_all_stellar_params_generate_without_exception(self):
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]

        for param in _starPars:
            # print(param, [eval('star.'+param) for star in starlist])
            fig = GeneralPlotter(starlist, param, 'R').plot()

    def test_mix_of_planet_and_star_classes_on_input_raises_TypeError(self):
        planetlist = generate_list_of_planets(3)
        starlist = [planet.star for planet in planetlist]

        with self.assertRaises(TypeError):
            fig = GeneralPlotter(planetlist + starlist)
            fig._set_axis('R', None)

    def test_set_axis_with_multi_unit_compound_unit_scaling(self):
        planetlist = generate_list_of_planets(3)
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius

        kmhr = aq.CompoundUnit('km / hr**2')

        fig = GeneralPlotter(planetlist)
        # for some reason the items equal assert fails, comparing the str representations is equivilent with strict order
        self.assertItemsAlmostEqual(fig._set_axis('calcSurfaceGravity()', kmhr),  # have not verfied values
        (52417.5200676341 * kmhr, 13104.380016908524 * kmhr, 5824.1688964037885 * kmhr), 4)

    def test_set_axis_with_multi_unit_non_compound_unit_scaling(self):
        planetlist = generate_list_of_planets(3)
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius

        fig = GeneralPlotter(planetlist)

        self.assertItemsAlmostEqual(fig._set_axis('calcSurfaceGravity()', aq.km / aq.hr**2),
                                    (52417.5200676341 * aq.km/aq.h**2, 13104.380016908524 * aq.km/aq.h**2, 5824.1688964037885 * aq.km/aq.h**2), 4)