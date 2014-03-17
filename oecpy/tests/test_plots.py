import unittest

import numpy as np
import quantities as pq

from ..example import genExamplePlanet
from ..plots import DataPerParameterBin, GeneralPlotter
from .. import astroquantities as aq


class Test_DataPerParameterBin(unittest.TestCase):

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


def generate_list_of_planets(number):
    planetList = []
    for i in range(number):
        planetList.append(genExamplePlanet())
    return planetList


class Test_GeneralPlotter(unittest.TestCase):

    def test__init__(self):
        x = GeneralPlotter(generate_list_of_planets(3))

    def test_set_axis_with_variables(self):
        planetlist = generate_list_of_planets(3)
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius

        fig = GeneralPlotter(planetlist)
        self.assertItemsEqual(fig._set_axis('R'), radiusValues)

    def test_set_axis_with_functions(self):
        planetlist = generate_list_of_planets(3)
        radiusValues = (5*aq.R_j, 10*aq.R_j, 15*aq.R_j)

        for i, radius in enumerate(radiusValues):
            planetlist[i].params['radius'] = radius

        fig = GeneralPlotter(planetlist)
        results = fig._set_axis('calcDensity()')
        answer = (0.04138 * pq.g/pq.cm**3, 0.00517 * pq.g/pq.cm**3, 0.00153 * pq.g/pq.cm**3)

        self.assertEqual(len(results), len(answer))
        for i, result in enumerate(results):
            self.assertAlmostEqual(result, answer[i], 4)