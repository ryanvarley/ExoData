""" Handles database classes including search functions
"""

import re

compactString = lambda string: string.replace(' ','').replace('-','').lower()


class OECDatabase(object):
    """ This Class Handles the OEC database including search functions.
    """

    def __init__(self, planets):
        """ Initial implementation of DBclass. Will eventually take over a lot of the code in the exoplanetcatalogue.py

        currently only takes the planet list as input as the class on handles search
        """

        self.planets = planets
        self.planetSearchDict = self._generatePlanetSearchDict(planets)

    def searchPlanet(self, name):
        """ Searches the database for a planet. Input can be complete ie GJ1214b, alternate name variations or even
        just 1214.

        :param name: the name of the planet to search
        :return: dictionary of results as planetname -> planet object
        """

        searchName = compactString(name)
        returnSet = set()

        for altname, planetObj in self.planetSearchDict.iteritems():
            if re.search(searchName, altname):
                returnSet.add(planetObj.name)

        if returnSet:
            if len(returnSet) == 1:
                return self.planetSearchDict[returnSet.pop()]
            else:
                rlist = []

        else:
            return False

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

    def _generatePlanetSearchDict(self, planets):
        """ Generates a search dictionary for planets by taking all names and 'flattening' them to the most compact form
        (lowercase, no spaces and dashes)
        """

        planetNameDict = {}
        for planet in planets:

            name = planet.name
            altnames = planet.params['altnames']
            altnames.append(name)  # as we also want the default name to be searchable

            for altname in altnames:
                reducedname = compactString(altname)
                planetNameDict[reducedname] = planet

        return planetNameDict