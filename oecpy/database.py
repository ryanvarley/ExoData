""" Handles database classes including search functions
"""

import re
import xml.etree.ElementTree as ET
import glob
import os.path
import sys

# 2.6 patch for ExpatError being raised over ParseError (which didn't exist)
if sys.hexversion < 0x02070000:
    import xml.parsers.expat
    ET.ParseError = xml.parsers.expat.ExpatError

from .astroclasses import System, Binary, Star, Planet, Parameters, BinaryParameters, StarParameters, PlanetParameters

compactString = lambda string: string.replace(' ', '').replace('-', '').lower()


class OECDatabase(object):
    """ This Class Handles the OEC database including search functions.
    """

    def __init__(self, databaseLocation):
        """ Holds the Open Exoplanet Catalogue database in python

        :param databaseLocation: file path to the Open Exoplanet Catalogue systems folder ie
            ~/git/open-exoplanet-catalogue-atmospheres/systems/
            get the catalogue from https://github.com/hannorein/open_exoplanet_catalogue
        """

        self._loadDatabase(databaseLocation)
        self._planetSearchDict = self._generatePlanetSearchDict()

        self.systemDict = dict((system.name, system) for system in self.systems)
        self.binaryDict = dict((binary.name, binary) for binary in self.binaries)
        self.starDict = dict((star.name, star) for star in self.stars)
        self.planetDict = dict((planet.name, planet) for planet in self.planets)

    def __repr__(self):
        return 'OECDatabase({} Systems, {} Binaries, {} Stars, {} Planets)'.format(len(self.systems), len(self.binaries),
                                                                                   len(self.stars), len(self.planets))

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
                if planet.isTransiting:
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
        self.systems = []
        self.binaries = []
        self.stars = []
        self.planets = []

        databaseXML = glob.glob(os.path.join(databaseLocation, '*.xml'))
        if not len(databaseXML):
            raise LoadDataBaseError('could not find the database xml files. Have you given the correct location to the open exoplanet catalogues /systems folder?')

        for filename in databaseXML:
            try:
                tree = ET.parse(open(filename, 'r'))
            except ET.ParseError as e:  # this is sometimes raised rather than the root.tag system check
                raise LoadDataBaseError(e)

            root = tree.getroot()

            # Process the system
            if not root.tag == 'system':
                raise LoadDataBaseError('file {0} does not contain a valid system - could be an error with your version'
                                        ' of the catalogue'.format(filename))

            systemParams = Parameters()
            for systemXML in root:

                tag = systemXML.tag
                text = systemXML.text
                attrib = systemXML.attrib

                systemParams.addParam(tag, text, attrib)

            system = System(systemParams.params)
            self.systems.append(system)  # Add system to the index

            self._loadBinarys(root, system)
            self._loadStars(root, system)

    def _loadBinarys(self, parentXML, parent):

        binarysXML = parentXML.findall("binary")

        for binaryXML in binarysXML:
            binaryParams = BinaryParameters()

            for value in binaryXML:

                tag = value.tag
                text = value.text
                attrib = value.attrib

                binaryParams.addParam(tag, text, attrib)

            binary = Binary(binaryParams.params)
            binary.parent = parent

            parent._addChild(binary)  # Add star to the system

            self._loadBinarys(binaryXML, binary)
            self._loadStars(binaryXML, binary)
            self._loadPlanets(binaryXML, binary)  # Load planets

            self.binaries.append(binary)  # Add star to the index

    def _loadStars(self, parentXML, parent):

        starsXML = parentXML.findall("star")

        for starXML in starsXML:
            starParams = StarParameters()

            for value in starXML:

                tag = value.tag
                text = value.text
                attrib = value.attrib

                starParams.addParam(tag, text, attrib)

            star = Star(starParams.params)
            star.parent = parent

            parent._addChild(star)  # Add star to the system

            self._loadPlanets(starXML, star)  # Load planets

            self.stars.append(star)  # Add star to the index

    def _loadPlanets(self, parentXML, parent):

        planetsXML = parentXML.findall("planet")

        for planetXML in planetsXML:

            planetParams = PlanetParameters()

            for value in planetXML:

                tag = value.tag
                text = value.text
                attrib = value. attrib

                planetParams.addParam(tag, text, attrib)

            planet = Planet(planetParams.params)
            planet.parent = parent

            parent._addChild(planet)  # Add planet to the star
            self.planets.append(planet)  # Add planet to the index


class LoadDataBaseError(IOError):
    pass