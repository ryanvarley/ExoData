""" This is a large test designed to find bugs in the code and errors in the
 database
"""

from .patches import TestCase
from .. import database

exocat = database.load_db_from_url()


class TestCatalogue_Planet(TestCase):

    def test_isTransiting(self):
        x = [planet.isTransiting for planet in exocat.planets]

    def test_calcTransitDuration(self):
        x = [planet.calcTransitDuration() for planet in exocat.planets]

    def test_calcTransitDuration_circular(self):
        x = [planet.calcTransitDuration(circular=True) for planet in exocat.planets]

    def test_a(self):
        x = [planet.a for planet in exocat.planets]

    def test_e(self):
        x = [planet.e for planet in exocat.planets]

    def test_i(self):
        x = [planet.i for planet in exocat.planets]

    def test_T(self):
        x = [planet.T for planet in exocat.planets]

    def test_albedo(self):
        x = [planet.albedo for planet in exocat.planets]


class TestCatalogue_Star(TestCase):

    def test_magV(self):
        x = [star.magV for star in exocat.stars]

    def test_T(self):
        x = [star.T for star in exocat.stars]

    def test_calcTemperature(self):
        x = [star.calcTemperature() for star in exocat.stars]