""" This module handles any assumptions the rest of the package uses.

Im not sure how to best implement assumptions that are fully flexible to the user. This could be how the planet type
is defined or other characteristics. Im using a simple 'OK' method here, overwriting assumptions would require loading
this module and defining or changing the variables.

If anyone has a good solution to this issue, please create it in a fork or email me!
"""

import quantities as pq
import astroquantities as aq

# TODO open an issue about this module for community discussion

planetAssumptions = {
    # Contains all planet assumptions, the key refers to the type of assumption and the format of the value can vary
    # based on the type of assumption

    'massType':
        [
            # Planet types are defined by their Mass, using inf as an absolute upper limit
            # the format of the tuples are (mass upperlimit, name). The current format dosn't allow overlaps and must be
            # in order. If you append a value run .sort() after.
            (5 * aq.M_e, 'Super-Earth'),
            (15 * aq.M_e, 'Neptune'),
            (300 * aq.M_e, 'Jupiter')  # 'possible' off the scale. can use float('inf') to avoid
        ],

    'radiusType': # TODO interface with rest of module
        [
            (1.8 * aq.R_e, 'Super-Earth'),
            (4 * aq.R_e, 'Neptune'),
            (10 * aq.R_e, 'Jupiter')  # 'possible' off the scale. can use float('inf') to avoid
        ],

    'tempType':
        [
            (320 * pq.K, 'Temperate'),
            (600 * pq.K, 'Warm'),
            (1500 * pq.K, 'Hot'),
            (float('inf'), 'Very Hot'),
        ],

    'mu':  # depends on masstype so takes the masstype as the key, and mu as the value
        {
            'Super-Earth': 18 * pq.atomic_mass_unit,  # TODO these should be more inherently linked to masstype
            'Neptune': 2 * pq.atomic_mass_unit,
            'Jupiter': 2 * pq.atomic_mass_unit
        },

    'albedo':  # depends on temperature so it takes tempType as the key and the albedo as the value
        {
            'Temperate': 0.3,
            'Warm': 0.3,
            'Hot': 0.1
        }
    
}


def planetMassType(mass):
    """ Returns the planet masstype given the mass and using planetAssumptions['massType']
    """

    for massLimit, massType in planetAssumptions['massType']:

        if mass < massLimit:
            return massType


def planetTempType(temperature):
    """ Returns the planet masstype given the temperature and using planetAssumptions['tempType']
    """

    for tempLimit, tempType in planetAssumptions['tempType']:

        if temperature < tempLimit:
            return tempType


def planetType(temperature, mass):
    """ Returns the planet type as 'temperatureType massType'
    """

    return '{} {}'.format(planetTempType(temperature), planetMassType(mass))


def planetMu(massType):
    return planetAssumptions['mu'][massType]


def planetAlbedo(tempType):
    return planetAssumptions['albedo'][tempType]