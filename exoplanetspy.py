""" This module is an interface for the open exoplanet catalogue. Its design motive is to be user friendly and readable
with speed as a secondary consideration. Therefore if your using larger complex queries and are comfortable with the
default xml.etree.ElementTree you will probably find that faster and more powerful.
"""

import xml.etree.ElementTree as ET
import glob

from astroclasses import System, Star, Planet
from os.path import basename

databaseLocation = '/Users/ryanv/Documents/git/open-exoplanet-catalogue/systems/'  # Temp

# Initialise Database
systems = {}
stars = {}
planets = {}

for filename in glob.glob(databaseLocation + '*.xml'):
    tree = ET.parse(open(filename, 'r'))
    root = tree.getroot()

    # Process the system
    assert root.tag == 'system', '{} does not contain a valid system'  # TODO remove or upgrade to raise or try

    systemParams = {}
    for systemXML in root:

        tag = systemXML.tag

        if not tag == 'star':  # TODO this is for the class to reject not the loader
            systemParams[tag] = systemXML.text

    system = System(systemParams)
    systems[system.params['name']] = system  # Add system to the index

    # Now look for stars
    starsXML = root.findall(".//star")

    for starXML in starsXML:

        starParams = {}

        for value in starXML:

            tag = value.tag

            if not tag == 'planet':  # TODO this is for the class to reject not the loader
                starParams[tag] = value.text

        star = Star(starParams)
        star.parent = system

        stars[star.params['name']] = star  # Add planet to the index


















