""" Contains structural classes ie binary, star, planet etc which mimic the xml structure with objects
"""
import equations as eq
import quantities as pq


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


class System(baseObject):

    @property
    def ra(self):
        return self.params['rightascension']

    @property
    def dec(self):
        return self.params['declination']

    @property
    def d(self):
        return self.params['distance']


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
        return self.params['radius']

    @property
    def T(self):
        return self.params['temperature']

    @property
    def M(self):
        return self.params['mass']


class Star(StarAndPlanetCommon):

    def calcLuminosity(self):

        return eq.starLuminosity(self.R, self.T)

    @property
    def Z(self):
        return self.params['metallicity']

    @property
    def magV(self):
        return self.params['magV']

    @property
    def spectralType(self):
        return self.params['spectraltype']


class Planet(StarAndPlanetCommon):

    def isTransiting(self):
        """ Checks the discovery method to see if the planet transits
        """

        if self.params['discoverymethod'] == 'transit':
            return True  # is this all or will it miss RV detected planets that transit?
        else:
            return False

    def calcTansitDuration(self):
        """ Estimation of the primary transit time assuming a circular orbit (see :py:func:`equations.transitDuration`)
        """

        return eq.transitDuration(self.P, self.parent.R, self.R, self.a, self.i)

    def calcSurfaceGravity(self):

        return eq.surfaceGravity(self.M, self.R)

    def calcLogg(self):

        return eq.logg(self.M, self.R)

    def calcMeanTemp(self):
        raise NotImplementedError
        # return eq.meanPlanetTemp()  # TODO implement albedo assumptions

    def calcScaleHeight(self):
        raise NotImplementedError
        # return eq.scaleHeight(self.T, , self.g)  # TODO mu based on assumptions

    def planetType(self):
        raise NotImplementedError  # TODO based on assumptions


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
            'mass': pq.M_s,
            'metallicity': 1,
            'radius': pq.R_s,
            'magV': 1,
        })


class PlanetParameters(Parameters):

    def __init__(self):

        Parameters.__init__(self)

        self._defaultUnits.update({
            'mass': pq.M_j,
            'radius': pq.R_j,
            'inclination': pq.deg,
            'eccentricity': 1,
            'period': pq.day,
            'semimajoraxis': pq.au
        })