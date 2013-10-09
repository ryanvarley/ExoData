"""
Contains code for simulating observations and calculating signal to noise of various targets. The module was stolen
from another private project and so contains a few equations i left in incase anyone finds them useful.

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

from __future__ import division
from numpy import sqrt, arcsin, sin, cos, log10, nan

import quantities as pq
import quantities.constants as const
import astroquantities as aq

pi = const.pi
sigma = const.Stefan_Boltzmann_constant
G = const.Newtonian_constant_of_gravitation


def scaleHeight(T_eff_p, mu_p, g_p):
    """ Caculate the scale height H of the atmosphere

    .. math::
        H = \\frac{k T_eff}{\mu g}

    Where H is the scale height of the planets atmosphere, :math:`T_eff` is the planetary effective temperature,
    :math:`\mu` is the mean molecular weight of the planetary atmosphere and g is the planets surface gravity.

    :param T_eff_p: Effective temperature
    :param mu: mean molecular weight
    :param g: surface gravity
    :return: H (scale Height)
    """

    # TODO allow overwrite of scale heights assumed in atmosphere

    H = (const.k * T_eff_p) / (mu_p * g_p)
    return H.rescale(pq.m)


def meanPlanetTemp(A_p, T_s, R_s, a):
    """ Calculate the equilibrium planet temperature

    assumes epsilon = 0.7 http://arxiv.org/pdf/1111.1455v2.pdf
    """

    T_p = T_s * ((1-A_p)/0.7)**(1/4) * sqrt(R_s/(2*a))

    return T_p.rescale(pq.degK)


def starLuminosity(R_s, T_eff):
    """ Calculate stellar luminosity

    .. math::
        L_\star = 4\pi R^2_\star \sigma T^4_\star

    Where :math:`L_\star` is the Stellar luminosity, :math:`R_\star` stellar radius, :math:`\sigma` Stefan-Boltzman
    constant, :math:`T_\star` the temperature of the star

    :param R: stellar radius
    :param T_eff: effective surface temperature of the star
    :return: :math:`L_\star`
    """

    L_s = 4 * pi * R_s**2 * sigma * T_eff**4

    return L_s.rescale(pq.W)


def ratioTerminatorToStar(H_p, R_p, R_s):  # TODO use this in code with scale height calc
    """ Calculates the ratio of the terminator to the star assuming 5 scale heights large. If you dont know all of the
    input try :py:func:`calcRatioTerminatorToStar`

    .. math::
        \Delta F = \\frac{10 H R_p + 25 H^2}{R_\star^2}

    Where :math:`\Delta F` is the ration of the terminator to the star, H scale height planet atmosphere,
    :math:`R_p` radius of the planet, :math:`R_s` raidus of the star

    :param H_p:
    :param R_p:
    :param R_s:
    :return: ratio of the terminator to the star
    """
    # TODO let user overwrite scale heights and auto function to select on planet type?

    deltaF = ((10 * H_p * R_p) + (25 * H_p**2)) / (R_s**2)
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


def surfaceGravity(M_p, R_p):
    """ Calculates the surface acceleration due to gravity on the planet

    .. math::
        g_p = \\frac{GM_p}{R_p^2}

    where :math:`g_p` is the acceleration ude to gravity on the planet surface, G is the gravitational constant,
    :math:`M_p` planetary mass, :math:`R_p` radius of the planet

    :param params: dict containing 'M_p', 'R_p' with units

    :return: g - acceleration due to gravity * m / s**2
    """

    # TODO find out what logg is and how it can be used

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


def transitDuration(P, R_s, R_p, a, i):
    """ Estimation of the primary transit time. Assumes a circular orbit.

    .. Note: This code could do with reverifing and perhaps using the eccentricity version

    .. math::
        T_\\text{dur} = \\frac{P}{\pi}\sin^{-1} \left[\\frac{R_\star}{a}\\frac{\sqrt{(1+k)^2 + b^2}}{\sin{a}} \\right]

    Where :math:`T_\\text{dur}` transit duration, P orbital period, :math:`R_\star` radius of the star,
    a is the semi-major axis, k is :math:`\\frac{R_p}{R_s}`

    :param i: orbital inclination
    :return:
    """

    # TODO use non circular orbit version?
    if i is nan:
        i = 90 * pq.deg

    i = i.rescale(pq.rad)
    k = R_p / R_s  # lit reference for eclipsing binaries
    b = (a * cos(i)) / R_s

    duration = (P / pi) * arcsin(((R_s * sqrt((1 + k) ** 2 - b ** 2)) / (a * sin(i))).simplified)

    return duration.rescale(pq.min)


def logg(M_p, R_p):
    """ Calculates the surface acceleration due to gravity on the planet as logg, the base 10 logarithm of g in cgs
    units. This function uses :py:func:`surfaceGravity` and then rescales it to cgs and takes the log
    """

    g = surfaceGravity(M_p, R_p)
    logg = log10(float(g.rescale(pq.cm / pq.s**2)))  # the float wrapper is needed to remove dimensionality

    return logg


def starTemperature(M_s):
    """ Estimates stellar temperature using the main sequence relationship T ~ 5800*M^0.65
    """
    return (5800*pq.K * float(M_s.rescale(aq.M_s)**0.65)).rescale(pq.K)


def transitDepth(R_s, R_p):
    """ Calculates the transit depth
    """

    depth = (R_p / R_s)**2

    return depth.rescale(pq.dimensionless)


def density(M, R):
    """ Calculates the density in g/cm**3
    :param R: radius
    :param M: mass
    :return:
    """

    volume = 4 / 3 * pi * R**3

    return (M/volume).rescale(pq.g / pq.cm**3)


def estimateMass(R, density):
    """ Estimates mass based on radius and a density
    :param R: Radius
    :param density: density to calculate mass from
    :return: mass
    """

    volume = 4 / 3 * pi * R**3

    return (density * volume).rescale(aq.M_j)


def calcSemiMajorAxis(Period, M_s):
    """ Calculates the semi-major axis of the orbit using the period and stellar mass

    .. math::
        a = \left( \frac{Period^2 G M_s}{4*\pi^2} \right))^{1/3}
    """
    a = ((Period**2 * G * M_s)/(4 * pi**2))**(1/3)

    return a.rescale(pq.au)


def calcSemiMajorAxis2(T_p, T_s, A_p, R_s, epsilon=0.7):
    """ Calculates the semi-major axis of the orbit using the planet temperature

    .. math::
        a = \text{tbc}
    """
    a = sqrt((1-A_p)/epsilon) * (R_s/2) * (T_s/T_p)**2

    return a.rescale(pq.au)


def calcPeriod(a, M_s):
    """ Calculates the period of the orbit using the stellar mass and sma
    :return:

    .. math::
        a = \text{tbc}
    """

    P = 2 * pi * sqrt(a**3 / (G * M_s))

    return P.rescale(pq.day)


# TODO more orbital equations