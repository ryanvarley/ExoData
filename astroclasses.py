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