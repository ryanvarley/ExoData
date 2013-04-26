""" This module handles any assumptions the rest of the package uses.

Im not sure how to best implement assumptions that are fully flexible to the user. This could be how the planet type
is defined or other charcterisitics. Im using a simple 'OK' method here, overwriting assumptions would require loading
this module and defining or changing the variables.

If anyone has a good solution to this issue, please create it in a fork or email me!
"""

import quantities as pq

# TODO open an issue about this module for community discussion

planetAssumptions = {
    # Contains all planet assumptions, the key refers to the type of assumption and the format of the value can vary
    # based on the type of assumption

    'massType':
        [
            # Planet types are defined by their Mass, using inf as an absolute upper limit
            # the format of the tuples are (mass upperlimit, name). The current format dosn't allow overlaps and must be
            # in order. If you append a value run .sort() after.
            (0.35 * pq.M_j, 'Super-Earth'),
            (0.7 * pq.M_j, 'Neptune'),
            (float('inf'), 'Jupiter')
        ],

    'tempType':
        [
            (350 * pq.K, 'Habitable'),
            (800* pq.K, 'Warm'),
            (float('inf'), 'Hot'),
        ]

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

