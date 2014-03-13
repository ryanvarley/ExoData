import unittest
from collections import OrderedDict

import numpy as np

from ..example import genExamplePlanet
from ..plots import DataPerParameterBin
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