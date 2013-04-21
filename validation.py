"""
Contains code for various user input data validation applicable to the module
"""

import quantities as pq

stdUnitParamDict = {
    'R_s': pq.R_s,  # Radius Star
    'M_s': pq.M_s,  # Mass of Star
    'T_eff_s': pq.degK,  # Effective temperature of the star
    'L_s': pq.W,  # Luminosity of Star
    'Mag_V': pq.dimensionless,  # Vega Magnitude


    'R_p': pq.R_j,  # Radius Planet
    'M_p':  pq.M_j,  # Mass Planet
    'T_eff_p': pq.degK,  # Effective temperature of the planet
    'mu_p': pq.u,  # mean molecular weight
    'A_p': pq.dimensionless,  # Albedo (bond)
    'g_p': pq.m / pq.s**2,  # acceleration due to gravity
    'H_p': pq.m,  # scale height

    'i': pq.deg,  # Inclintion
    'e': pq.dimensionless,  # orbit eccentricity
    'a': pq.au,  # Semi-Major Axis of the planet-star orbit
    'P': pq.day,  # Orbital Period
}


def checkPlanetParamsAndUnits(params, paramList=None, unitParamDict=None):
    """ Checks the key, values in params against the key, units in paramDict to make sure the params are present
    and of the right unit type.

    :param params: planet params Dict
    :param paramList: parameters to check (if not all in params)
    :param unitParamDict: Dictionary to get key -> unit combinations from. If none pulls the stdUnitParamDict
    :return:
    """

    if type(params) is not dict:
        raise(TypeError, 'params type must be Dict got {}'.format(type(params)))

    if paramList is None:
        paramList = params.iterkeys()

    if unitParamDict is None:
        unitParamDict = stdUnitParamDict

    for param in paramList:

        dimensions = params[param] / unitParamDict[param]

        try:
            dimensions.rescale(pq.dimensionless)
        except ValueError:
            raise ValueError('{} must be of unit type {} got {}'.format(param, unitParamDict[param], params[param]))





