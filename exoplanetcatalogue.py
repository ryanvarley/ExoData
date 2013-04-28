""" This module is an interface for the open exoplanet catalogue. Its design motive is to be user friendly and readable
with speed as a secondary consideration. Therefore if your using larger complex queries and are comfortable with the
default xml.etree.ElementTree you will probably find that faster and more powerful.
"""

import xml.etree.ElementTree as ET
import glob

from astroclasses import System, Star, Planet, Parameters, StarParameters, PlanetParameters
from database import OECDatabase

databaseLocation = '/Users/ryanv/Documents/git/open-exoplanet-catalogue-atmospheres/systems/'  # Temp

# Initialise Database
systems = {}
stars = {}
planets = {}

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
    systems[system.name] = system  # Add system to the index

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
        stars[star.name] = star  # Add star to the index

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
            planets[planet.name] = planet  # Add planet to the index


# Initialise the db (will take over in future)
db = OECDatabase(planets)  # Use db.searchPlanet(name) to find a planet

