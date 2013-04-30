""" Handles database classes including search functions
"""

import re
import xml.etree.ElementTree as ET
import glob

from astroclasses import System, Star, Planet, Parameters, StarParameters, PlanetParameters

compactString = lambda string: string.replace(' ', '').replace('-', '').lower()


class OECDatabase(object):
    """ This Class Handles the OEC database including search functions.
    """

    def __init__(self, databaseLocation):
        """ Hold the Open Exoplanet Catalogue database in python

        :param databaseLocation: file path to the Open Exoplanet Catalogue systems folder ie
            ~/git/open-exoplanet-catalogue-atmospheres/systems/
            get the catalogue from https://github.com/hannorein/open_exoplanet_catalogue
        """

        self._loadDatabase(databaseLocation)
        self._planetSearchDict = self._generatePlanetSearchDict()

    def searchPlanet(self, name):
        """ Searches the database for a planet. Input can be complete ie GJ1214b, alternate name variations or even
        just 1214.

        :param name: the name of the planet to search
        :return: dictionary of results as planetname -> planet object
        """

        searchName = compactString(name)
        returnDict = {}

        for altname, planetObj in self._planetSearchDict.iteritems():
            if re.search(searchName, altname):
                returnDict[planetObj.name] = planetObj

        if returnDict:
            if len(returnDict) == 1:
                return returnDict.values()[0]
            else:
                return returnDict.values()

        else:
            return False

    @property
    def transitingPlanets(self):
        """ Returns a list of transiting planet objects
        """

        transitingPlanets = []

        for planet in self.planets:
            try:
                if planet.isTransiting():
                    transitingPlanets.append(planet)
            except KeyError:  # No 'discoverymethod' tag - this also filters Solar System planets
                pass

        return transitingPlanets

    def _generatePlanetSearchDict(self):
        """ Generates a search dictionary for planets by taking all names and 'flattening' them to the most compact form
        (lowercase, no spaces and dashes)
        """

        planetNameDict = {}
        for planet in self.planets:

            name = planet.name
            altnames = planet.params['altnames']
            altnames.append(name)  # as we also want the default name to be searchable

            for altname in altnames:
                reducedname = compactString(altname)
                planetNameDict[reducedname] = planet

        return planetNameDict

    def _loadDatabase(self, databaseLocation):
        """ Loads the database from a given file path in the class
        """

        # Initialise Database
        systems = []
        stars = []
        planets = []

        for filename in glob.glob(databaseLocation + '*.xml'):
            tree = ET.parse(open(filename, 'r'))
            root = tree.getroot()

            # Process the system
            assert root.tag == 'system', '{} does not contain a valid system'  # TODO remove or upgrade to raise or try

            systemParams = Parameters()
            for systemXML in root:

                tag = systemXML.tag
                text = systemXML.text
                attrib = systemXML.attrib

                systemParams.addParam(tag, text, attrib)

            system = System(systemParams.params)
            systems.append(system)  # Add system to the index

            # Now look for stars
            starsXML = root.findall(".//star")

            for starXML in starsXML:

                starParams = StarParameters()

                for value in starXML:

                    tag = value.tag
                    text = value.text
                    attrib = value.attrib

                    starParams.addParam(tag, text, attrib)

                star = Star(starParams.params)
                star.parent = system

                system._addChild(star.name, star)  # Add star to the system
                stars.append(star)  # Add star to the index

                # And finally look for planets
                planetsXML = root.findall(".//planet")

                for planetXML in planetsXML:

                    planetParams = PlanetParameters()

                    for value in planetXML:

                        tag = value.tag
                        text = value.text
                        attrib = value. attrib

                        planetParams.addParam(tag, text, attrib)

                    planet = Planet(planetParams.params)
                    planet.parent = star

                    star._addChild(planet.name, planet)  # Add planet to the star
                    planets.append(planet)  # Add planet to the index

        self.planets, self.stars, self.systems = planets, stars, systems