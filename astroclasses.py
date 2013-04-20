""" Contains structural classes ie binary, star, planet etc which mimic the xml structure with objects
"""


class baseObject(object):

    def __init__(self, params=None):

        self.children = {}
        self.parent = None

        self.params = {}
        self._updateParams(self._initialParams())

        self._updateParams(params)  # TODO value validator?

    def _addChild(self, name, child):

        self.children.update({name: child})

    def _updateParams(self, params):
        """ This method updates parameters allowing for any validation / unit additions in the near future
        """

        self.params.update(params)

    def _initialParams(self):

        return {}  # Only used in child classes


class System(baseObject):

    def _initialParams(self):

        systemParams = {
            'name': None,
            'rightascension': None,
            'declination': None,
            'distance': None,
            }

        return systemParams


class Star(baseObject):

    def _initialParams(self):

        starParams = {
            'name': None,
            }

        return starParams


class Planet(baseObject):

    pass

    def _calculateTransit(self):  # for a getter to pull .isTransiting from
        pass


class Parameters(dict):  # TODO would this subclassing dict be more preferable?
    """ A class to hold parameter dictionaries, the input can be validated, units added and handling of multi valued
    fields. In future this may be better as a child of dict.
    """

    def __init__(self):

        self.params = {
            'altnames': [],
        }

    def addParam(self, key, value):
        """ Checks the key dosnt already exist, adds alternate names to a sperate list

        Future
            - format input and add units
            - reject parent tags
            - logging
        """

        if key in self.params:

            if key is 'name':
                self.params['altnames'].append(value)

            else:
                pass  # TODO: log rejected value

        else:  # If the key dosnt already exist

            # TODO check if its a nested class (ie /n...)

            self.params[key] = value


