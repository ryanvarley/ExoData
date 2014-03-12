import unittest
from collections import OrderedDict

from ..example import genExamplePlanet
from ..plots import DataPerParameterBin
from .. import astroquantities as aq


class Test_DataPerParameterBin(unittest.TestCase):

    def testDataGeneratesCorrectly(self):
        planets = {}
        #                eccentricity, pri, sec, both
        planetInfoList = ([0, True, True, 1],
                          [0.1, True, True, 1],
                          [0.2, True, True, 1],
                          [0.3, True, True, 1],
                          [0.45, True, True, 1],
                          [0.5, True, True, 1],
                          [0.6, True, True, 1],

                          [0.1, True, False, 0.5],
                          [0.4, False, True, 0.5],
                          [0.5, False, False, 0],)

        for planetInfo in planetInfoList:
            planet = genExamplePlanet()
            planet.params['eccentricity'] = planetInfo[0]
            planets[planet.name] = {'planet': planet, 'resolutions': {'5050303030':{ 'observable_pri': planetInfo[1], 'observable_sec': planetInfo[2],
                            'rating': planetInfo[3]}}}

        results = planets

        data = DataPerParameterBin(results, 'e', (0, 0.2, 0.4, 0.6))
        # TODO fails because now used ordered dict so must set up than add as parsing a dict to it wont be ordered.
        answer = {'sec': {'0 to 0.2': 2, '0.2 to 0.4': 2, '0.4 to 0.6': 4, 'Uncertain': 0},
                  'pri': {'0 to 0.2': 3, '0.2 to 0.4': 2, '0.4 to 0.6': 3, 'Uncertain': 0},
                  'both': {'0 to 0.2': 3, '0.2 to 0.4': 2, '0.4 to 0.6': 4, 'Uncertain': 0}}

        self.assertDictEqual(answer, data._processResults())

    def test_limits_generated_correctly(self):
        planets = {}
        #                eccentricity, pri, sec, both
        planetInfoList = ([-10, True, True, 1],
                          [1, True, True, 1],
                          [10, True, True, 1],)

        for planetInfo in planetInfoList:
            planet = genExamplePlanet()
            planet.params['eccentricity'] = planetInfo[0]
            planets[planet.name] = {'planet': planet, 'resolutions': {'5050303030':{'planet': planet, 'observable_pri': planetInfo[1], 'observable_sec': planetInfo[2],
                            'rating': planetInfo[3]}}}

        results = planets
        data = DataPerParameterBin(results, 'e', (-float('inf'), 0, 5, float('inf')))

        answer = {'sec': {'<0': 1, '0 to 5': 1, '5+': 1, 'Uncertain': 0},
                  'pri': {'<0': 1, '0 to 5': 1, '5+': 1, 'Uncertain': 0},
                  'both': {'<0': 1, '0 to 5': 1, '5+': 1, 'Uncertain': 0}}

        self.assertDictEqual(answer, data._processResults())

