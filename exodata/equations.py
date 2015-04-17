"""
Contains code for simulating observations and calculating signal to noise of various targets.

**Abbreviations used in this module**

* R_p - Planetary Radius
* M_p - Planetary Mass
* M_s - Stellar Mass
* R_s - Stellar Radius
* H - Scale height of the Planets Atmosphere
* i - orbital inclination
* e - orbit eccentricity
* T_eff_s - Effective Temperature of the Star
* A - Albedo
* mu - mean molecular weight
"""

from __future__ import division
from numpy import sqrt, arcsin, sin, cos, log10, nan

import numpy as np
import os
import sys
from pkg_resources import resource_stream, resource_filename
import math

import quantities.constants as const
from . import astroquantities as aq


pi = const.pi
sigma = const.Stefan_Boltzmann_constant
G = const.Newtonian_constant_of_gravitation

_rootdir = os.path.dirname(__file__)


def scaleHeight(T_eff_p, mu_p, g_p):
    """ Calculate the scale height H of the atmosphere

    .. math::
        H = \\frac{k T_eff}{\mu g}

    Where H is the scale height of the planets atmosphere, :math:`T_{eff}` is the planetary effective temperature,
    :math:`\mu` is the mean molecular weight of the planetary atmosphere and g is the planets surface gravity.

    :param T_eff_p: Effective temperature
    :param mu: mean molecular weight
    :param g: surface gravity
    :return: H (scale Height)
    """

    H = (const.k * T_eff_p) / (mu_p * g_p)
    return H.rescale(aq.m)


def meanPlanetTemp(A_p, T_s, R_s, a, e=0.7):
    """ Calculate the equilibrium planet temperature

    .. math::


    assumes epsilon = 0.7 by default http://arxiv.org/pdf/1111.1455v2.pdf
    """

    T_p = T_s * ((1-A_p)/e)**(1/4) * sqrt(R_s/(2*a))

    return T_p.rescale(aq.degK)


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

    return L_s.rescale(aq.W)


def ratioTerminatorToStar(H_p, R_p, R_s):  # TODO add into planet class
    """ Calculates the ratio of the terminator to the star assuming 5 scale heights large. If you dont know all of the
    input try :py:func:`calcRatioTerminatorToStar`

    .. math::
        \Delta F = \\frac{10 H R_p + 25 H^2}{R_\star^2}

    Where :math:`\Delta F` is the ration of the terminator to the star, H scale height planet atmosphere,
    :math:`R_p` radius of the planet, :math:`R_s` radius of the star

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

    g_p = (G * M_p)/(R_p**2)
    return g_p.rescale(aq.m / aq.s**2)


def calcRatioTerminatorToStar(params):  # TODO update with new format
    """ Calculates the ratio of the Terminator to the Star using :py:func:`ratioTerminatorToStar` but calculates all
    intermediary params on route.

    This is a convenience function which will largely be used over the others as the intermediary params arent often given
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
    a is the semi-major axis, k is :math:`\\frac{R_p}{R_s}`, b is :math:`\frac{a}{R_*} \cos{i}` (Seager & Mallen-Ornelas 2003)

    :param i: orbital inclination
    :return:
    """

    # TODO use non circular orbit version?
    if i is nan:
        i = 90 * aq.deg

    i = i.rescale(aq.rad)
    k = R_p / R_s  # lit reference for eclipsing binaries
    b = (a * cos(i)) / R_s

    duration = (P / pi) * arcsin(((R_s * sqrt((1 + k) ** 2 - b ** 2)) / (a * sin(i))).simplified)

    return duration.rescale(aq.min)


def logg(M_p, R_p):
    """ Calculates the surface acceleration due to gravity on the planet as logg, the base 10 logarithm of g in cgs
    units. This function uses :py:func:`surfaceGravity` and then rescales it to cgs and takes the log
    """

    g = surfaceGravity(M_p, R_p)
    logg = log10(float(g.rescale(aq.cm / aq.s**2)))  # the float wrapper is needed to remove dimensionality

    return logg


def estimateStarTemperature(M_s):
    """ Estimates stellar temperature using the main sequence relationship T ~ 5800*M^0.65 (Cox 2000)??
    """
    # TODO improve with more x and k values from Cox 2000
    return (5800*aq.K * float(M_s.rescale(aq.M_s)**0.65)).rescale(aq.K)


def transitDepth(R_s, R_p):
    """ Calculates the transit depth
    """

    depth = (R_p / R_s)**2

    return depth.rescale(aq.dimensionless)


def density(M, R):
    """ Calculates the density in g/cm**3
    :param R: radius
    :param M: mass
    :return:
    """

    volume = 4 / 3 * pi * R**3

    return (M/volume).rescale(aq.g / aq.cm**3)


def estimateMass(R, density):
    """ Estimates mass based on radius and a density
    :param R: Radius
    :param density: density to calculate mass from
    :return: mass
    """

    volume = 4 / 3 * pi * R**3

    return (density * volume).rescale(aq.M_j)


def estimateStellarRadius(M_s):
    """ Estimates radius from mass based on stellar type
    .. math::
        R_* = k M^x_*
    where k is a constant coefficient for each stellar sequence anad x describes the power law of the sequence
    (Seager & Mallen-Ornelas 2003).
    """

    x = 0.8
    k = False

    R = k * M_s^x

    return NotImplementedError


def calcSemiMajorAxis(Period, M_s):
    """ Calculates the semi-major axis of the orbit using the period and stellar mass

    .. math::
        a = \left( \frac{P^2 G M_*}{4*\pi^2} \right))^{1/3}

    """
    a = ((Period**2 * G * M_s)/(4 * pi**2))**(1/3)

    return a.rescale(aq.au)


def calcSemiMajorAxis2(T_p, T_s, A_p, R_s, epsilon=0.7):
    """ Calculates the semi-major axis of the orbit using the planet temperature

    .. math::
        a = \sqrt\frac{1-A_p}{\epsilon} \frac{R_\star}{2} \left(\frac{T_\star}{T_p}\right)^2
    """
    a = sqrt((1-A_p)/epsilon) * (R_s/2) * (T_s/T_p)**2

    return a.rescale(aq.au)


def calcPeriod(a, M_s, M_p=0.*aq.M_e):
    """ Calculates the period of the orbit using the stellar mass, planet mass and sma using keplers Third Law
    :return:

    .. math::
        P = \sqrt{\frac{4\pi^2a^3}{G \left(M_\star + M_p \right)}}
    """

    P = 2 * pi * sqrt(a**3 / (G * (M_s + M_p)))

    return P.rescale(aq.day)


def impactParameter(a, R_s, i):
    """ projected distance between the planet and star centers during mid transit
    .. math::
        b \equiv \frac{a}{R_*} \cos{i}
    (Seager & Mallen-Ornelas 2003).
    """
    b = (a/R_s) * cos(i.rescale(aq.rad))

    return b.rescale(aq.dimensionless)


def estimateDistance(m, M, Av=0.0):
    """ estimate the distance to star based on the absolute magnitude, apparent magnitude and the
    absorbtion / extinction

    :param m: apparent magnitude
    :param M: absolute magnitude
    :param Av: absorbtion / extinction

    :return: d (distance to object) in parsecs
    """
    try:
        m = float(m)  # basic value checking as there is no units
        M = float(M)
        Av = float(Av)
    except TypeError:
        return np.nan

    d = 10**((m-M+5-Av)/5)

    if math.isnan(d):
        return np.nan
    else:
        return d * aq.pc


def _createAbsMagEstimationDict():
    """ loads magnitude_estimation.dat which is from http://xoomer.virgilio.it/hrtrace/Sk.htm on 24/01/2014 and
    based on Schmid-Kaler (1982)

    creates a dict in the form [Classletter][ClassNumber][List of values for each L Class]
    """
    magnitude_estimation_filepath = resource_filename(__name__, 'data/magnitude_estimation.dat')
    raw_table = np.loadtxt(magnitude_estimation_filepath, '|S5')

    absMagDict = {'O': {}, 'B': {}, 'A': {}, 'F': {}, 'G': {}, 'K': {}, 'M': {}}
    for row in raw_table:
        if sys.hexversion >= 0x03000000:
            starClass = row[0].decode("utf-8")  # otherwise we get byte ints or b' caused by 2to3
            absMagDict[starClass[0]][int(starClass[1])] = [float(x) for x in row[1:]]
        else:
            absMagDict[row[0][0]][int(row[0][1])] = [float(x) for x in row[1:]]  # dict of spectral type = {abs mag for each luminosity class}

    # manually typed from table headers - used to match columns with the L class (header)
    LClassRef = {'V': 0, 'IV': 1, 'III': 2, 'II': 3, 'Ib': 4, 'Iab': 5, 'Ia': 6, 'Ia0': 7}

    return absMagDict, LClassRef

absMagDict, LClassRef = _createAbsMagEstimationDict()


def estimateAbsoluteMagnitude(spectralType):
    """ Uses the spectral type to lookup an approximate absolute magnitude for the star.
    """

    from .astroclasses import SpectralType

    specType = SpectralType(spectralType)

    if specType.classLetter == '':
        return np.nan
    elif specType.classNumber == '':
        specType.classNumber = 5  # aproximation using mid magnitude value

    if specType.lumType == '':
        specType.lumType = 'V'  # assume main sequence

    LNum = LClassRef[specType.lumType]
    classNum = specType.classNumber
    classLet = specType.classLetter

    try:
        return absMagDict[classLet][classNum][LNum]
    except (KeyError, IndexError):  # value not in table. Assume the number isn't there (Key p2.7, Ind p3+)
        try:
            classLookup = absMagDict[classLet]
            values = np.array(list(classLookup.values()))[:, LNum]  # only select the right L Type
            return np.interp(classNum, list(classLookup.keys()), values)
        except (KeyError, ValueError):
            return np.nan  # class not covered in table


def _createMagConversionDict():
    """ loads magnitude_conversion.dat which is table A% 1995ApJS..101..117K
    """
    magnitude_conversion_filepath = resource_stream(__name__, 'data/magnitude_conversion.dat')
    raw_table = np.loadtxt(magnitude_conversion_filepath, '|S5')

    magDict = {}
    for row in raw_table:
        if sys.hexversion >= 0x03000000:
            starClass = row[1].decode("utf-8")  # otherwise we get byte ints or b' caused by 2to3
            tableData = [x.decode("utf-8") for x in row[3:]]
        else:
            starClass = row[1]
            tableData = row[3:]
        magDict[starClass] = tableData

    return magDict

magDict = _createMagConversionDict()


def magKtoMagV(*args, **kwargs):
    """ Converts K magnitude to V magnitude
    """
    raise DeprecationWarning("This function has is been phased out in favour of the astroclasses.Magnitude class which can"
                             " convert between many magnitudes")

# TODO more orbital equations