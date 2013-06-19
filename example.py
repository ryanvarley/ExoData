""" Code to contain example and other empty classes mainly for tests
"""

# I am making a make system so that unit tests in EASE can load fake targets that will stay constant for the tests
# Due to its wider applicability im putting these here

from astroclasses import Planet, Star, System, Parameters, PlanetParameters, StarParameters

import astroquantities as aq
import quantities as pq

systemPar = Parameters()
systemPar.addParam('name', 'Example System')
systemPar.addParam('distance', 58)
systemPar.addParam('declination', '+04 05 06')
systemPar.addParam('rightascension', '01 02 03')

# TODO Binary

starPar = StarParameters()
starPar.addParam('age', '7.6')
starPar.addParam('magB', '9.8')
starPar.addParam('magH', '7.4')
starPar.addParam('magI', '7.6')
starPar.addParam('magJ', '7.5')
starPar.addParam('magK', '7.3')
starPar.addParam('magV', '9.0')
starPar.addParam('mass', '0.98')
starPar.addParam('metallicity', '0.43')
starPar.addParam('name', 'Example Star')
starPar.addParam('name', 'HD Example Star')
starPar.addParam('radius', '0.95')
starPar.addParam('spectraltype', 'G5')
starPar.addParam('temperature', '5370')

planetPar = PlanetParameters()
planetPar.addParam('discoverymethod', 'transit')
planetPar.addParam('discoveryyear', '2001')
planetPar.addParam('eccentricity', '0.09')
planetPar.addParam('inclination', '89.2')
planetPar.addParam('lastupdate', '12/12/08')
planetPar.addParam('mass', '3.9')
planetPar.addParam('name', 'Example Star b')
planetPar.addParam('period', '111.2')
planetPar.addParam('radius', '0.92')
planetPar.addParam('semimajoraxis', '0.449')
planetPar.addParam('temperature', '339.6')
planetPar.addParam('transittime', '2454876.344')

exampleSystem = System(systemPar.params)
exampleStar = Star(starPar.params)
examplePlanet = Planet(planetPar.params)

exampleSystem._addChild(exampleStar)
exampleStar._addChild(examplePlanet)
examplePlanet.parent = exampleStar
exampleStar.parent = exampleSystem

# TODO add heirarchy