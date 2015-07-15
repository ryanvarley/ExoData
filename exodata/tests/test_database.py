import unittest
from tempfile import mkdtemp, mkstemp
import shutil

from .. import OECDatabase, load_db_from_url  # load from root
from ..database import LoadDataBaseError
from .patches import TestCase

from .. import astroquantities as aq


class TestDataBaseLoading(TestCase):

    def setUp(self):
        # create temp dir
        self.tempDir = mkdtemp()
        self._createFakeXML()
        self.oecdb = OECDatabase(self.tempDir + '/')

    def _createFakeXML(self):

        xmlCases = [
            "<system><name>System 1</name><star><name>Star 1</name></star></system>",  # System -> star

            "<system><name>System 2</name><star><name>Star 2</name>"  # system -> star -> planet
            "<planet><name>Planet 2 b</name></planet></star></system>",

            "<system><name>System 3</name><star><name>Star 3</name>"  # system -> star -> planet, planet
            "<planet><name>Planet 3 b</name></planet><planet><name>Planet 3 c</name></planet></star></system>",

            "<system><name>System 4</name>"  # system -> binary -> (star -> planet), star
            "<binary><name>Binary 4AB</name><star><name>Star 4A</name>"
            "<planet><name>Planet 4A b</name></planet></star><star><name>Star 4B</name></star></binary></system>",

            "<system><name>System 5</name>"  # system -> binary -> star, binary -> star, (star -> planet)
            "<binary><name>Binary 5AB</name><star><name>Star 5A</name></star>"
            "<binary><name>Binary 5B-AB</name><star><name>Star 5B-A</name>"
            "<planet><name>Planet 5B-A b</name></planet></star><star><name>Star 5B-B</name></star>"
            "</binary></binary></system>",

            "<system><name>System 6</name>"  # system -> binary -> star, star, planet
            "<binary><name>Binary 6AB</name><star><name>Star 6A</name></star>"
            "<star><name>Star 6B</name></star>"
            "<planet><name>Planet 6AB b</name></planet></binary></system>",

            "<system><name>System 7</name><star><name>Star 7</name>"  # system -> star -> planet (seperation unit)
            '<planet><name>Planet 7 b</name><separation unit="arcsec">2.2</separation>'
			'<separation unit="AU">330</separation></planet></star></system>',
        ]

        for systems in xmlCases:
            with open(mkstemp('.xml', dir=self.tempDir)[1], 'w') as f:
                f.write(systems)

    def test_correct_system_number(self):
        self.assertEqual(len(self.oecdb.systems), 7)

    def test_correct_star_only_system(self):  # 1
        system = self.oecdb.systemDict['System 1']

        self.assertEqual(str(system.children), "[Star('Star 1')]")
        self.assertEqual(system.children[0].children, [])

    def test_correct_star_planet_system(self):  # 2
        system = self.oecdb.systemDict['System 2']

        self.assertEqual(str(system.children), "[Star('Star 2')]")
        self.assertEqual(str(system.children[0].children), "[Planet('Planet 2 b')]")

    def test_correct_star_double_planet_system(self):  # 3
        system = self.oecdb.systemDict['System 3']

        self.assertEqual(str(system.children), "[Star('Star 3')]")
        self.assertEqual(str(system.children[0].children), "[Planet('Planet 3 b'), Planet('Planet 3 c')]")

    def test_correct_binary_star_planet_system(self):  # 4
        system = self.oecdb.systemDict['System 4']

        self.assertEqual(str(system.children), "[Binary('Binary 4AB')]")
        self.assertEqual(str(system.children[0].children), "[Star('Star 4A'), Star('Star 4B')]")
        self.assertEqual(str(system.children[0].children[0].children), "[Planet('Planet 4A b')]")
        self.assertEqual(system.children[0].children[1].children, [])

    def test_correct_double_binary_star_planet_system(self):
        system = self.oecdb.systemDict['System 5']

        self.assertEqual(str(system.children), "[Binary('Binary 5AB')]")
        self.assertEqual(str(system.children[0].children), "[Binary('Binary 5B-AB'), Star('Star 5A')]")
        self.assertEqual(str(system.children[0].children[0].children), "[Star('Star 5B-A'), Star('Star 5B-B')]")
        self.assertEqual(str(system.children[0].children[0].children[0].children), "[Planet('Planet 5B-A b')]")
        self.assertEqual(system.children[0].children[1].children, [])
        self.assertEqual(system.children[0].children[0].children[1].children, [])

    def test_correct_binary_planet_star_system(self):
        system = self.oecdb.systemDict['System 6']

        self.assertEqual(str(system.children), "[Binary('Binary 6AB')]")
        self.assertEqual(str(system.children[0].children), "[Star('Star 6A'), Star('Star 6B'), Planet('Planet 6AB b')]")
        self.assertEqual(system.children[0].children[0].children, [])
        self.assertEqual(system.children[0].children[1].children, [])

    def test_seperation_tag_AU_imported_only(self):  # TODO code full solution
        system = self.oecdb.systemDict['System 7']

        self.assertEqual(system.children[0].children[0].separation, 330 * aq.au)

    def tearDown(self):
        shutil.rmtree(self.tempDir)


class TestDataBaseFailing(TestCase):

    def setUp(self):
        self.tempDir = mkdtemp()

    def test_raises_LoadDataBaseError_in_empty_folder(self):

        with self.assertRaises(LoadDataBaseError):
            OECDatabase(self.tempDir)

    def test_raises_LoadDataBaseError_without_system_tag(self):
        xmlCases = [
            "<name>System 1</name><star><name>Star 1</name></star>",
            "<star><name>Star 2</name>"  # system -> star -> planet
            "<planet><name>Planet 2 b</name></planet></star>",
        ]

        for systems in xmlCases:
            with open(mkstemp('.xml', dir=self.tempDir)[1], 'w') as f:
                f.write(systems)

        with self.assertRaises(LoadDataBaseError):
            OECDatabase(self.tempDir)

    def tearDown(self):
        shutil.rmtree(self.tempDir)


class Test_load_db_from_url(TestCase):

    def test_autoload(self):
        exocat = load_db_from_url()  # Note will fail without internet connection

        self.assertTrue(len(exocat.planets) > 1000)
        self.assertTrue(len(exocat.systems) > 1000)
        self.assertTrue(len(exocat.stars) > 1000)


if __name__ == '__main__':
    unittest.main()
