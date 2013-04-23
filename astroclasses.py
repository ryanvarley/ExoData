""" Contains structural classes ie binary, star, planet etc which mimic the xml structure with objects
"""

try:
    import quantities as pq
    unitsEnabled = True
except ImportError:
    unitsEnabled = False


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
        raise NotImplementedError  # TODO

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
            return True
        else:
            return False

    def calcTansitDuration(self):
        """ Estimation of the primary transit time assuming a circular orbit (see :py:func:`equations.transitDuration`)
        """

    def calcSurfaceGravity(self):
        raise NotImplementedError  # TODO

    def calcMeanTemp(self):
        raise NotImplementedError  # TODO

    def calcScaleHeight(self):
        raise NotImplementedError  # TODO

    def planetType(self):
        raise NotImplementedError  # TODO


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
        }

        self._defaultUnits = self._getDefaultUnits()

        self.rejectTags = ('system', 'star', 'planet', 'moon')  # These are handled in their own classes

    def addParam(self, key, value):
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
            else:
                print 'rejected duplicate {}: {}'.format(key, value)  # TODO: log rejected value
                return False  # TODO Replace with exception

        else:  # If the key dosnt already exist and isn't rejected
            if unitsEnabled:
                if key in self._defaultUnits:
                    value *= self._defaultUnits[key]
            self.params[key] = value

    def add_units(self):
        pass

    def _getDefaultUnits(self):
        """ This lists the default units for database parameters in order to add them to values being imported
        """

        defaults = {
            'temperature': pq.K,
        }
        return defaults


class StarParameters(Parameters):

    def _getDefaultUnits(self):
        """ This lists the default units for database parameters in order to add them to values being imported
        """

        parentDefaults = Parameters._getDefaultUnits()

        defaults = {
            'mass': pq.M_s,
            'metallicity': None,
            'radius': pq.R_s,
            'magV': None,
        }

        return parentDefaults.update(defaults)


class PlanetParameters(Parameters):

    def _getDefaultUnits(self):
        """ This lists the default units for database parameters in order to add them to values being imported
        """

        parentDefaults = Parameters._getDefaultUnits()

        defaults = {
            'mass': pq.M_j,
            'radius': pq.R_j,
            'inclination': pq.deg,
            'eccentricity': None,
            'period': pq.day,
            'semimajoraxis': pq.au
        }

        return parentDefaults.update(defaults)


