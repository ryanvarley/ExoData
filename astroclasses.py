""" Contains structural classes ie binary, star, planet etc which mimic the xml structure with objects
"""


class baseObject(object):

    def __init__(self, params=None):

        self.children = {}
        self.parent = None

        self.params = {}

    def _addChild(self, name, child):

        self.children.update({name: child})

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

            self.params[key] = value


