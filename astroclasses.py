""" Contains structural classes ie binary, star, planet etc which mimic the xml structure with objects
"""
import numpy as np

import quantities as pq

import equations as eq
import astroquantities as aq
import assumptions as assum


class baseObject(object):

    def __init__(self, params=None):

        self.children = {}
        self.parent = None

        self.params = {}
        self._updateParams(params)  # TODO value validator?

    def _addChild(self, name, child):

        self.children.update({name: child})

    def _updateParams(self, params):
        """ This method updates parameters allowing for any validation / unit additions in the near future
        """

        self.params.update(params)

    @property
    def name(self):
        return self.params['name']

    def __repr__(self):
        return 'baseObject({!r})'.format(self.name)

    def getParam(self, paramKey):
        """ Fetches a parameter from the params dictionary. If it's not there it will return NaN. This allows the use
        of list comprehensions over the entire planet set without KeyErrors.

        NaN was used as unlike False and None, NaN < 1 and NaN > 1 are both False
        """

        try:
            return self.params[paramKey]
        except KeyError:
            return np.NaN


class System(baseObject):

    @property
    def ra(self):
        return self.getParam('rightascension')

    @property
    def dec(self):
        return self.getParam('declination')

    @property
    def d(self):
        return self.getParam('distance')

    def __repr__(self):
        return 'System({!r})'.format(self.name)

    @property
    def stars(self):
        return self.children


class StarAndPlanetCommon(baseObject):

    @property  # allows stars and planets to access system values by propagating up
    def ra(self):
        return self.parent.ra

    @property
    def dec(self):
        return self.parent.dec

    @property
    def d(self):
        return self.parent.d

    @property
    def R(self):
        return self.getParam('radius')

    @property
    def T(self):
        return self.getParam('temperature')

    @property
    def M(self):
        return self.getParam('mass')

    def __repr__(self):
        return 'StarAndPlanetCommon({!r})'.format(self.name)

    @property
    def system(self):
        return self.parent

    def calcSurfaceGravity(self):

        return eq.surfaceGravity(self.M, self.R)

    def calcLogg(self):

        return eq.logg(self.M, self.R)


class Star(StarAndPlanetCommon):

    def calcLuminosity(self):

        return eq.starLuminosity(self.R, self.T)

    @property
    def Z(self):
        return self.getParam('metallicity')

    @property
    def magV(self):
        return self.getParam('magV')

    @property
    def spectralType(self):
        return self.getParam('spectraltype')

    @property
    def planets(self):
        return self.children

    def __repr__(self):
        return 'Star({!r})'.format(self.name)


class Planet(StarAndPlanetCommon):

    def isTransiting(self):
        """ Checks the discovery method to see if the planet transits
        """

        if self.params['discoverymethod'] == 'transit':
            return True  # is this all or will it miss RV detected planets that transit?
        else:
            return False

    def calcTransitDuration(self):
        """ Estimation of the primary transit time assuming a circular orbit (see :py:func:`equations.transitDuration`)
        """

        return eq.transitDuration(self.P, self.parent.R, self.R, self.a, self.i)

    def calcMeanTemp(self):
        raise NotImplementedError
        # return eq.meanPlanetTemp()  # TODO implement albedo assumptions

    def calcScaleHeight(self):
        raise NotImplementedError
        # return eq.scaleHeight(self.T, , self.g)  # TODO mu based on assumptions

    def type(self):
        return assum.planetType(self.T, self.M)

    def massType(self):
        return assum.planetMassType(self.M)

    def tempType(self):
        return assum.planetTempType(self.T)

    def mu(self):  # TODO make getter look in params first calc if not
        return assum.planetMu(self.massType())

    def albedo(self):
        return assum.planetAlbedo(self.tempType())

    @property
    def e(self):
        return self.params['eccentricity']

    @property
    def i(self):
        return self.params['inclination']

    @property
    def P(self):
        return self.params['period']

    @property
    def a(self):
        return self.params['semimajoraxis']

    @property
    def star(self):
        return self.parent

    def __repr__(self):
        return 'Planet({!r})'.format(self.name)


class Parameters(object):  # TODO would this subclassing dict be more preferable?
    """ A class to hold parameter dictionaries, the input can be validated, units added and handling of multi valued
    fields. In future this may be better as a child of dict.
    """

    def __init__(self):

        self.params = {
            'altnames': [],
            'list': [],
        }

        self._defaultUnits = {
            'temperature': pq.K,
            'distance': pq.pc,
        }

        self.rejectTags = ('system', 'star', 'planet', 'moon')  # These are handled in their own classes

    def addParam(self, key, value, attrib=None):
        """ Checks the key dosnt already exist, adds alternate names to a seperate list

        Future
            - format input and add units
            - logging
        """

        if key in self.rejectTags:
            return False  # TODO Replace with exception

        if key in self.params:

            if key == 'name':
                self.params['altnames'].append(value)
            elif key == 'list':
                self.params['list'].append(value)
            else:
                print 'rejected duplicate {}: {} in {}'.format(key, value, self.params['name'])  # TODO: log rejected value
                return False  # TODO Replace with exception

        else:  # If the key dosnt already exist and isn't rejected

            # Some tags have no value but a upperlimit in the attributes
            if value is None and attrib is not None:
                try:
                    value = attrib['upperlimit']
                except KeyError:
                    try:
                        value = attrib['lowerlimit']
                    except KeyError:
                        return False

            if key in self._defaultUnits:
                try:
                    value = float(value) * self._defaultUnits[key]
                except:
                    print 'caught an error with {} - {}'.format(key, value)
            self.params[key] = value


class StarParameters(Parameters):

    def __init__(self):

        Parameters.__init__(self)

        self._defaultUnits.update({
            'mass': aq.M_s,
            'metallicity': 1,
            'radius': aq.R_s,
            'magV': 1,
        })


class PlanetParameters(Parameters):

    def __init__(self):

        Parameters.__init__(self)

        self._defaultUnits.update({
            'mass': aq.M_j,
            'radius': aq.R_j,
            'inclination': pq.deg,
            'eccentricity': 1,
            'period': pq.day,
            'semimajoraxis': pq.au
        })