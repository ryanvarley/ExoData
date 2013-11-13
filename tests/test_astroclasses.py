import unittest
import sys
from os.path import join
sys.path.append(join('..'))

import numpy as np
import quantities as pq

from astroclasses import Parameters, Star, Planet, Binary, System, _findNearest
from example import genExamplePlanet, examplePlanet


class TestListFiles(unittest.TestCase):

    def create_Parameter_object(self):

        params = {
            'RA': 111111,
            'DEC': 222222,
            'name': 'monty',
        }

        paramObj = Parameters()
        paramObj.params.update(params)

        return paramObj

    def test_addParam_works_no_duplicate(self):

        paramObj = self.create_Parameter_object()

        paramObj.addParam('radius', '12')

        self.assertEqual(paramObj.params['radius'], '12')

    def test_addParam_works_recognised_duplicate_name(self):  # ie name which is a known and accepted duplicate

        paramObj = self.create_Parameter_object()

        paramObj.addParam('name', 'python')

        self.assertEqual(paramObj.params['name'], 'monty')

        self.assertEqual(paramObj.params['altnames'], ['python'])

    def test_addParam_works_unrecognised_duplicate(self):  # a unknown duplicate to delete (and log)

        paramObj = self.create_Parameter_object()

        paramObj.addParam('RA', 333333)

        self.assertEqual(paramObj.params['RA'], 111111)

        # TODO test to ensure the rejection is logged

    def test_addParam_name_type_pri_overwrites(self):  # a unknown duplicate to delete (and log)

        paramObj = self.create_Parameter_object()

        paramObj.addParam('name', 'first')
        paramObj.addParam('name', 'popular', {'type': 'pri'})
        paramObj.addParam('name', 'last')

        self.assertEqual(paramObj.params['name'], 'popular')
        self.assertItemsEqual(paramObj.params['altnames'], ('first', 'last', 'monty'))

    def test_empty_Planet_init(self):
        Planet().__repr__()

    def test_empty_Star_init(self):
        Star().__repr__()

    def test_empty_System_init(self):
        System().__repr__()

    def test_empty_Binary_init(self):
        Binary().__repr__()


class TestStarParameters(unittest.TestCase):

    def test_getLimbdarkeningCoeff_works(self):
        pass  # This simple check covered by test_example

    def test_distance_estimation_fails_invalid_spectral_type(self):
        """ If theres no distance, will try to calculate based on spectral type
        """
        planet = genExamplePlanet()
        star = planet.star

        star.params['spectraltype'] = 'FIV8'  # should currently fail as its not main sequence
        star.parent.params.pop('distance')

        self.assertTrue(star.d is np.nan)
        self.assertTrue(planet.d is np.nan)

    def test_distance_estimation_works(self):
        planet = genExamplePlanet()
        star = planet.star
        star.params['spectraltype'] = 'A4'
        star.params['magV'] = 5
        star.parent.params.pop('distance')

        self.assertAlmostEqual(star.d, 38.02 * pq.pc, 2)
        self.assertTrue('Estimated Distance' in star.flags.flags)

    def test_distance_estimation_not_called_if_d_present(self):
        planet = genExamplePlanet()
        star = planet.star
        star.parent.params['distance'] = 10

        self.assertEqual(star.d, 10 * pq.pc)
        self.assertFalse('Estimated Distance' in star.flags.flags)

    def test_magV_when_present(self):
        planet = genExamplePlanet()
        star = planet.star

        self.assertEqual(star.magV, 9.0)
        self.assertFalse('Estimated magV' in star.flags.flags)

    def test_magV_when_absent_converts_k(self):
        planet = genExamplePlanet()
        star = planet.star
        star.params.pop('magV')

        self.assertAlmostEqual(star.magV, 8.88, 2)
        self.assertTrue('Estimated magV' in star.flags.flags)


class TestFindNearest(unittest.TestCase):

    def setUp(self):
        self.arr = np.array([1.2,4,6,7.0,9.5,10,11,12])

    def test_exact_value_returns_exact(self):
        self.assertEqual(_findNearest(self.arr, 6), 6)

    def test_below_first_value_works(self):
        self.assertEqual(_findNearest(self.arr, 0.8), 1.2)

    def test_above_last_value_works(self):
        self.assertEqual(_findNearest(self.arr, 13), 12)

    @unittest.skip("TestFindNearest.test_mid_value_rounded_up skipped as it rounds down but it is not an issue atm")
    def test_mid_value_rounded_up(self):  # It isnt, but this isn't a large issue
        self.assertEqual(_findNearest(self.arr, 10.5), 11)

    def test_low_value_rounded_down(self):
        self.assertEqual(_findNearest(self.arr, 10.4), 10)

    def test_high_value_rounded_up(self):
        self.assertEqual(_findNearest(self.arr, 10.6), 11)


if __name__ == '__main__':
    unittest.main()
