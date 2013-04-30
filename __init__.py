""" This package is an interface for the open exoplanet catalogue. Its design motive is to be user friendly and readable
with speed as a secondary consideration. Therefore if your using larger complex queries and are comfortable with the
default xml.etree.ElementTree you will probably find that faster for basic queries.
"""

from database import OECDatabase
import equations
import assumptions