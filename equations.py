"""
Contains code for simulating observations and calculating signal to noise of various targets

The idea is this can contain the equations and pull info on the stars from tempfunctions (and later from OEC)

Functions in this module mostly take input from a params file. This is designed to be entered in advance or pulled
from a database. Units are entered using the py:module:`quantities`.

**Abbreviations used in this module**

* R_p - Planetary Radius
* M_p - Planetary Mass
* M_s - Stellar Mass
* R_s - Stellar Radius
* H - Scale height of the Planets Atmosphere
* i - orbital inclination
* e - orbit eccentricity
* T_eff_s - Effective Temperature Star
* A - Albedo
* mu - mean molecular weight
"""

from __future__ import division, print_function

from numpy import sqrt, arcsin, sin, cos

import quantities as pq
import quantities.constants as const
from ease.easesetup.validation import checkPlanetParamsAndUnits


pi = const.pi
sigma = const.Stefan_Boltzmann_constant
G = const.Newtonian_constant_of_gravitation

# TODO investigate impact of data 'prevalidation' could do a try, except to give the same info with lower overhead


def scaleHeight(params):
    """ Caculate the scale height H of the atmosphere

    .. math::
        H = \\frac{k T_p}{\mu g}

    Where H is the scale height of the planets atmosphere, :math:`T_p` is the planetary temperature,
    :math:`\mu` is the mean molecular weight of the planetary atmosphere and g is the planets surface gravity.

    :param params: dict containing 'T_eff_p', 'mu_p', 'g_p'
    :return: H (scale Height)
    """

    # TODO allow overwrite of scale heights assumed in atmosphere

    checkPlanetParamsAndUnits(params, ('T_eff_p', 'mu_p', 'g_p'))

    T_p = params['T_eff_p']
    mu = params['mu_p']
    g = params['g_p']

    H = (const.k * T_p) / (mu * g)
    return H.rescale(pq.m)


def meanPlanetTemp(params):
    """ Calculate the equilibrium planet temperature

    .. math::
        T_p = \left[\\frac{(1-A)L_\star}{16 \\times \sigma\pi a^2}\\right]^{1/4}

    Where :math:`T_p` is the equilibrium temperature of the planet, :math:`L_\star` is the stellar Luminosity,
    A is the bond albedo of the planet, :math:`\sigma` is the Stefan-Boltzman constant, a is the semi-major axis.

    :param params: dict containing 'A_p', 'L_s', 'a'
    :return: :math:`T_p` (mean temp of planet)
    """

    checkPlanetParamsAndUnits(params, ('A_p', 'L_s', 'a'))

    A = params['A_p']
    L_s = params['L_s']
    a = params['a']

    T_p = (((1 - A) * L_s) / (16 * sigma * pi * a**2))**(1 / 4)

    return T_p.rescale(pq.degK)


def starLuminosity(params):
    """ Calculate stellar luminosity

    .. math::
        L_\star = 4\pi R^2_\star \sigma T^4_\star

    Where :math:`L_\star` is the Stellar luminosity, :math:`R_\star` stellar radius, :math:`\sigma` Stefan-Boltzman
    constant, :math:`T_\star` the temperature of the star

    :param params: dict containing 'A_p', 'L_s', 'a', 'Rstar'
    :return: :math:`L_\star`
    """

    checkPlanetParamsAndUnits(params, ('R_s', 'T_eff_s'))

    R_s = params['R_s']
    T_s = params['T_eff_s']

    L_s = 4 * pi * R_s**2 * sigma * T_s**4

    return L_s.rescale(pq.W)


def ratioTerminatorToStar(params):
    """ Calculates the ratio of the terminator to the star assuming 5 scale heights large. If you dont know all of the
    input try :py:func:`calcRatioTerminatorToStar`

    .. math::
        \Delta F = \\frac{10 H R_p + 25 H^2}{R_\star^2}

    Where :math:`\Delta F` is the ration of the terminator to the star, H scale height planet atmosphere,
    :math:`R_p` radius of the planet, :math:`R_s` raidus of the star

    :param params: dict containing 'H_p', 'R_p', 'R_s' with units
    :return: ratio of the terminator to the star
    """

    checkPlanetParamsAndUnits(params, ('H_p', 'R_p', 'R_s'))

    H = params['H_p']
    R_p = params['R_p']
    R_s = params['R_s']

    deltaF = ((10 * H * R_p) + (25 * H**2)) / (R_s**2)
    return deltaF.simplified


def SNRPlanet(SNRStar, starPlanetFlux, Nobs, pixPerbin, NVisits=1):
    """ Calculate the Signal to Noise Ratio of the planet atmosphere

    .. math::
        \\text{SNR}_\\text{planet} = \\text{SNR}_\\text{star} \\times \Delta F \\times \sqrt{N_\\text{obs}}
        \\times \sqrt{N_\\text{pixPerbin}} \\times \sqrt{N_\\text{visits}}

    Where :math:`\\text{SNR}_\star` SNR of the star detection, :math:`\Delta F` ratio of the terminator to the star,
    :math:`N_\\text{obs}` number of exposures per visit, :math:`N_\\text{pixPerBin}` number of pixels per wavelength bin
    , :math:`N_\\text{visits}` number of visits

    :return:
    """

    SNRplanet = SNRStar * starPlanetFlux * sqrt(Nobs) * sqrt(pixPerbin) * sqrt(NVisits)

    return SNRplanet


def surfaceGravity(params):
    """ Calculates the surface acceleration due to gravity on the planet

    .. math::
        g_p = \\frac{GM_p}{R_p^2}

    where :math:`g_p` is the acceleration ude to gravity on the planet surface, G is the gravitational constant,
    :math:`M_p` planetary mass, :math:`R_p` radius of the planet

    :param params: dict containing 'M_p', 'R_p' with units

    :return: g - acceleration due to gravity * m / s**2
    """

    checkPlanetParamsAndUnits(params, ('M_p', 'R_p'))

    M_p = params['M_p']
    R_p = params['R_p']

    g_p = (G * M_p)/(R_p**2)
    return g_p.rescale(pq.m / pq.s**2)


def calcRatioTerminatorToStar(params):
    """ Calculates the ratio of the Terminator to the Star using :py:func:`ratioTerminatorToStar` but calculates all
    intermediary params on route.

    This is a conveince function which will largely be used over the others as the intermediary params arent often given
    in detection papers.

    :param params: dict containing ...
    :return: ratio of the terminator to the star
    """

    # check for optional params and calc if missing

    if 'H_p' not in params:
        if 'T_eff_p' not in params:
            if 'L_s' not in params:
                params['L_s'] = starLuminosity(params)
            params['T_eff_p'] = meanPlanetTemp(params)

        if 'g_p' not in params:
            params['g_p'] = surfaceGravity(params)

        params['H_p'] = scaleHeight(params)

    params['delta_F_p_s'] = ratioTerminatorToStar(params)

    return params['delta_F_p_s']


def transitDuration(params):
    """ Estimation of the primary transit time. Assumes a circular orbit.

    .. Note: This code could do with reverifing and perhaps using the eccentricity version

    .. math::
        T_\\text{dur} = \\frac{P}{\pi}\sin^{-1} \left[\\frac{R_\star}{a}\\frac{\sqrt{(1+k)^2 + b^2}}{\sin{a}} \\right]

    Where :math:`T_\\text{dur}` transit duration, P orbital period, :math:`R_\star` radius of the star,
    a is the semi-major axis, k is :math:`\\frac{R_p}{R_s}`

    :param params: dict with 'P', 'R_s', 'R_p', 'a', 'i' with units
    :return:
    """

    checkPlanetParamsAndUnits(params, ('P', 'R_s', 'R_p', 'a', 'i'))

    P = params['P']
    R_s = params['R_s']
    R_p = params['R_p']
    a = params['a']
    i = params['i'].rescale(pq.rad)
    k = R_p / R_s  # lit reference for eclipsing binaries
    b = (a * cos(i)) / R_s

    duration = (P / pi) * arcsin(((R_s * sqrt((1 + k) ** 2 - b ** 2)) / (a * sin(i))).simplified)

    return duration.rescale(pq.min)