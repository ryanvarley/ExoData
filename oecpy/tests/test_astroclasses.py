""" Note that many tests for the astroclasses are actually done in example. This is because this file generates fake
planets from which the tests can be ran. In future some xml could be included here for the same purpose.
"""

import sys
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest

import numpy as np
import quantities as pq

from ..astroclasses import Parameters, Star, Planet, Binary, System, _findNearest, SpectralType
from ..example import genExamplePlanet, examplePlanet
from .patches import TestCase


class TestListFiles(TestCase):

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

        star.params['spectraltype'] = 'C'  # should currently fail as its not main sequence
        star.parent.params.pop('distance')

        self.assertTrue(star.d is np.nan)
        self.assertTrue(planet.d is np.nan)

    def test_distance_estimation_works(self):
        planet = genExamplePlanet()
        star = planet.star
        star.params['spectraltype'] = 'A4'
        star.params['magV'] = 5
        star.parent.params.pop('distance')

        self.assertAlmostEqual(star.d, 45.19 * pq.pc, 2)
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

    def test_mid_value_rounded_down(self):  # Note this isn't what you may expect, but as long as we are aware of it
        self.assertEqual(_findNearest(self.arr, 10.5), 10)

    def test_low_value_rounded_down(self):
        self.assertEqual(_findNearest(self.arr, 10.4), 10)

    def test_high_value_rounded_up(self):
        self.assertEqual(_findNearest(self.arr, 10.6), 11)


class TestSpectralType(unittest.TestCase):

    def test_classType_and_Type(self):
        A8V = SpectralType('')
        A8V.lumType = 'V'
        A8V.classNumber = '8'
        A8V.classLetter = 'A'
        self.assertEqual(A8V.specClass, 'A8')
        self.assertEqual(A8V.specType, 'A8V')

    def test_works_normal_full_types(self):
        A8V = SpectralType('A8V')
        self.assertEqual(A8V.lumType, 'V')
        self.assertEqual(A8V.classLetter, 'A')
        self.assertEqual(A8V.classNumber, 8)

        L0IV = SpectralType('L0IV')
        self.assertEqual(L0IV.lumType, 'IV')
        self.assertEqual(L0IV.classLetter, 'L')
        self.assertEqual(L0IV.classNumber, 0)

    def test_works_single_letter(self):
        test1 = SpectralType('G')
        self.assertEqual(test1.lumType, '')
        self.assertEqual(test1.classLetter, 'G')
        self.assertEqual(test1.classNumber, '')

    def test_works_spec_class_only(self):
        A8 = SpectralType('A8')
        self.assertEqual(A8.lumType, '')
        self.assertEqual(A8.classLetter, 'A')
        self.assertEqual(A8.classNumber, 8)

        L0 = SpectralType('L0')
        self.assertEqual(L0.lumType, '')
        self.assertEqual(L0.classLetter, 'L')
        self.assertEqual(L0.classNumber, 0)

    def test_works_multiple_classes(self):
        test1 = SpectralType('K0/K1V')
        self.assertEqual(test1.lumType, '')
        self.assertEqual(test1.classLetter, 'K')
        self.assertEqual(test1.classNumber, 0)

        test2 = SpectralType('GIV/V')
        self.assertEqual(test2.lumType, 'IV')
        self.assertEqual(test2.classLetter, 'G')
        self.assertEqual(test2.classNumber, '')

        test3 = SpectralType('F8-G0')
        self.assertEqual(test3.lumType, '')
        self.assertEqual(test3.classLetter, 'F')
        self.assertEqual(test3.classNumber, 8)

    def test_works_spaces(self):
        test1 = SpectralType('K1 III')
        self.assertEqual(test1.lumType, 'III')
        self.assertEqual(test1.classLetter, 'K')
        self.assertEqual(test1.classNumber, 1)

    def test_works_decimal(self):
        test1 = SpectralType('K1.5III')
        self.assertEqual(test1.classLetter, 'K')
        self.assertEqual(test1.classNumber, 1.5)
        self.assertEqual(test1.lumType, 'III')

    def test_works_decmial_no_L_class(self):
        test2 = SpectralType('M8.5')
        self.assertEqual(test2.classLetter, 'M')
        self.assertEqual(test2.classNumber, 8.5)
        self.assertEqual(test2.lumType, '')

    def test_works_2_decimal_places(self):
        test2 = SpectralType('A9.67V')
        self.assertEqual(test2.classLetter, 'A')
        self.assertEqual(test2.classNumber, 9.67)
        self.assertEqual(test2.lumType, 'V')

    def test_works_no_number_after_decimal(self):
        test2 = SpectralType('B5.IV')
        self.assertEqual(test2.classLetter, 'B')
        self.assertEqual(test2.classNumber, 5)
        self.assertEqual(test2.lumType, 'IV')

    def test_works_2_letter_class(self):
        test2 = SpectralType('DQ6')
        self.assertEqual(test2.classLetter, 'DQ')
        self.assertEqual(test2.classNumber, 6)
        self.assertEqual(test2.lumType, '')

    def test_works_3_letter_class(self):
        test2 = SpectralType('DAV6')
        self.assertEqual(test2.classLetter, 'DAV')
        self.assertEqual(test2.classNumber, 6)
        self.assertEqual(test2.lumType, '')

        test3 = SpectralType('DA6')  # check two letter still works
        self.assertEqual(test3.classLetter, 'DA')
        self.assertEqual(test3.classNumber, 6)
        self.assertEqual(test3.lumType, '')

    def test_fake_3_letter_fails(self):
        test2 = SpectralType('DAX6')
        self.assertEqual(test2.classLetter, '')
        self.assertEqual(test2.classNumber, '')
        self.assertEqual(test2.lumType, '')

    def test_works_unknown_lum_class(self):
        test2 = SpectralType('G5D')
        self.assertEqual(test2.classLetter, 'G')
        self.assertEqual(test2.classNumber, 5)
        self.assertEqual(test2.lumType, '')

    def test_works_extra_info(self):
        test1 = SpectralType('K2 IV a')
        self.assertEqual(test1.lumType, 'IV')
        self.assertEqual(test1.classLetter, 'K')
        self.assertEqual(test1.classNumber, 2)

        test2 = SpectralType('G8 V+')
        self.assertEqual(test2.lumType, 'V')
        self.assertEqual(test2.classLetter, 'G')
        self.assertEqual(test2.classNumber, 8)

        test3 = SpectralType('G0V pecul.')
        self.assertEqual(test3.lumType, 'V')
        self.assertEqual(test3.classLetter, 'G')
        self.assertEqual(test3.classNumber, 0)

    def test_rejects_non_standard(self):
        # TODO rewrite with a list of cases to fail and for loop
        testStrings = ('Catac. var.', 'AM Her', 'nan', np.nan)

        for testStr in testStrings:
            test1 = SpectralType(testStr)
            self.assertEqual(test1.lumType, '', 'lumType null test for {0}'.format(testStr))
            self.assertEqual(test1.classLetter, '', 'classLetter null test for {0}'.format(testStr))
            self.assertEqual(test1.classNumber, '', 'classNumber null test for {0}'.format(testStr))
            self.assertEqual(test1.specType, '', 'specType null test for {0}'.format(testStr))


class TestPlanetClass(unittest.TestCase):

    def test_isTransiting_is_true_if_tag_present(self):
        planet = genExamplePlanet()
        planet.params['istransiting'] = '1'
        self.assertTrue(planet.isTransiting())

    def test_isTransiting_fails_with_missing_tag_or_incorrect_value(self):
        planet = genExamplePlanet()
        planet.params['istransiting'] = '0'
        self.assertFalse(planet.isTransiting())

        planet = genExamplePlanet()
        planet.params['istransiting'] = '2'
        self.assertFalse(planet.isTransiting())

        planet = genExamplePlanet()
        self.assertFalse(planet.isTransiting())


if __name__ == '__main__':
    unittest.main()
