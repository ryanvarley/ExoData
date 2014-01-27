""" Contains structural classes ie binary, star, planet etc which mimic the xml structure with objects
"""
import numpy as np
import os
import math

import quantities as pq

import equations as eq
import astroquantities as aq
import assumptions as assum
import flags


_rootdir = os.path.dirname(__file__)  # Get package directory


class baseObject(object):

    def __init__(self, params=None):

        self.children = []
        self.parent = None # TODO should be read only (use add method)
        self.classType = 'BaseObject'
        self.flags = flags.Flag()

        self.params = {}
        if params is not None:
            self._updateParams(params)  # TODO value validator?

    def _addChild(self, child):

        self.children.append(child)

    def _updateParams(self, params):
        """ This method updates parameters allowing for any validation / unit additions in the near future
        """

        self.params.update(params)

    @property
    def name(self):  # TODO variable for altnames
        try:
            return self.params['name']
        except KeyError:
            try:
                return self.parent.name
            except AttributeError:
                return 'Un-named ' + self.classType
        except AttributeError:
            return 'Un-named ' + self.classType

    def __repr__(self):
        return '{}({!r})'.format(self.classType, self.name)

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

    def __init__(self, *args, **kwargs):
        baseObject.__init__(self, *args, **kwargs)
        self.classType = 'System'

    @property
    def ra(self):
        return self.getParam('rightascension')

    @property
    def dec(self):
        return self.getParam('declination')

    @property
    def d(self):
        return self.getParam('distance')

    @property  # TODO could be binaries now, should differentiate
    def stars(self):
        return self.children


class StarAndPlanetCommon(baseObject):

    def __init__(self, *args, **kwargs):
        baseObject.__init__(self, *args, **kwargs)
        self.classType = 'StarAndPlanetCommon'

    @property
    def age(self):
        return self.getParam('age')

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
        """ Looks for the temperature in the catalogue, if absent it calculates it using calcTemperature()

        :return: planet temperature
        """
        paramTemp = self.getParam('temperature')

        if not paramTemp is np.nan:
            return paramTemp
        else:
            self.flags.addFlag('Calculated Temperature')
            return self.calcTemperature()

    @property
    def M(self):
        return self.getParam('mass')

    def calcTemperature(self):
        raise NotImplementedError('Only implemented for Stars and Planet child classes')

    @property  # TODO may return binary
    def system(self):
        return self.parent

    def calcSurfaceGravity(self):

        return eq.surfaceGravity(self.M, self.R)

    def calcLogg(self):

        return eq.logg(self.M, self.R)

    def calcDensity(self):

        if self.M is np.nan or self.R is np.nan:
            return np.nan
        else:
            return eq.density(self.M, self.R)


class Binary(StarAndPlanetCommon):  # TODO add binary methods and variables, remove unused one from starcommon

    def __init__(self, *args, **kwargs):
        StarAndPlanetCommon.__init__(self, *args, **kwargs)
        self.classType = 'Binary'

    @property
    def stars(self):
        return self.children


class Star(StarAndPlanetCommon):

    def __init__(self, *args, **kwargs):
        StarAndPlanetCommon.__init__(self, *args, **kwargs)
        self.classType = 'Star'

    @property
    def d(self):
        """ Note this should work from child parents as .d propergates, calculates using the star estimation method
        estimateDistance and estimateAbsoluteMagnitude
        """

        d = self.parent.d
        if d is np.nan:
            d = self.estimateDistance()
            if d is not np.nan:
                self.flags.addFlag('Estimated Distance')
        return d

    def calcLuminosity(self):

        return eq.starLuminosity(self.R, self.T)

    def calcTemperature(self):
        """ uses equations.starTemperature to estimate temperature based on main sequence relationship
        """
        return eq.starTemperature(self.M)

    @property
    def Z(self):
        return self.getParam('metallicity')

    @property
    def magB(self):
        return self.getParam('magB')

    @property
    def magH(self):
        return self.getParam('magH')

    @property
    def magI(self):
        return self.getParam('magI')

    @property
    def magJ(self):
        return self.getParam('magJ')

    @property
    def magK(self):
        return self.getParam('magK')

    @property
    def magV(self):
        magV = self.getParam('magV')
        if math.isnan(magV):
            if not math.isnan(self.magK):
                self.flags.addFlag('Estimated magV')
                magV = eq.magKtoMagV(self.spectralType, self.magK)
                if magV is None:  # eq sometimes outputs this
                    return np.nan
                else:
                    return magV
        if magV is None:  # if value is missing (particularly binaries) will return None for some reason
            return np.nan
        else:
            return magV

    @property
    def spectralType(self):
        return self.getParam('spectraltype')

    @property
    def planets(self):
        return self.children

    def getLimbdarkeningCoeff(self, wavelength=1.22):
        """ Looks up quadratic limb darkening parameter from the star based on T, logg and metalicity.

        :param wavelength: microns
        :type wavelength: float

        :return: limb darkening coefficients 1 and 2
        """

        # The intervals of values in the tables
        tempind = [ 3500., 3750., 4000., 4250., 4500., 4750., 5000., 5250., 5500., 5750., 6000., 6250.,
                 6500., 6750., 7000., 7250., 7500., 7750., 8000., 8250., 8500., 8750., 9000., 9250.,
                 9500., 9750., 10000., 10250., 10500., 10750., 11000., 11250., 11500., 11750., 12000., 12250.,
                 12500., 12750., 13000., 14000., 15000., 16000., 17000., 19000., 20000., 21000., 22000., 23000.,
                 24000., 25000., 26000., 27000., 28000., 29000., 30000., 31000., 32000., 33000., 34000., 35000.,
                 36000., 37000., 38000., 39000., 40000., 41000., 42000., 43000., 44000., 45000., 46000., 47000.,
                 48000., 49000., 50000.]
        lggind = [0., 0.5, 1., 1.5, 2., 2.5, 3., 3.5, 4., 4.5, 5.]
        mhind = [-5., -4.5, -4., -3.5, -3., -2.5, -2., -1.5, -1., -0.5, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.5, 1.]

        # Choose the values in the table nearest our parameters
        tempselect = _findNearest(tempind, float(self.T))
        lgselect = _findNearest(lggind, float(self.calcLogg()))
        mhselect = _findNearest(mhind, float(self.Z))

        coeffTable = np.loadtxt(os.path.join(_rootdir, "data", "quadratic.dat"))

        foundValues = False
        for i in xrange(len(coeffTable)):
            if coeffTable[i, 2] == lgselect and coeffTable[i, 3] == tempselect and coeffTable[i, 4] == mhselect:
                if coeffTable[i, 0] == 1:
                    u1array = coeffTable[i, 8:]  # Limb darkening parameter u1 for each wl in waveind
                    u2array = coeffTable[i+1, 8:]
                    foundValues = True
                    break

        if not foundValues:
            raise ValueError('No limb darkening values could be found')  # TODO replace with better exception

        waveind = [0.365, 0.445, 0.551, 0.658, 0.806, 1.22, 1.63, 2.19, 3.45]  # Wavelengths available in table

        # Interpolates the value at wavelength from values in the table (waveind)
        u1AtWavelength = np.interp(wavelength, waveind, u1array, left=0, right=0)
        u2AtWavelength = np.interp(wavelength, waveind, u2array, left=0, right=0)

        return u1AtWavelength, u2AtWavelength

    def estimateAbsoluteMagnitude(self):
        return eq.estimateAbsoluteMagnitude(self.spectralType)

    def estimateDistance(self):
        # TODO handle other mags than V
        if self.magV is not np.nan:
            return eq.estimateDistance(self.magV, self.estimateAbsoluteMagnitude())
        else:
            return np.nan


class Planet(StarAndPlanetCommon):

    def __init__(self, *args, **kwargs):
        StarAndPlanetCommon.__init__(self, *args, **kwargs)
        self.classType = 'Planet'

    def isTransiting(self):
        """ Checks the discovery method to see if the planet transits
        """

        if self.params['discoverymethod'] == 'transit':
            return True  # is this all or will it miss RV detected planets that transit?
        elif self.R is not np.nan:
            return True  # transit is the only method to give R
        else:
            return False

    def calcTransitDuration(self):
        """ Estimation of the primary transit time assuming a circular orbit (see :py:func:`equations.transitDuration`)
        """
        try:
            return eq.transitDuration(self.P, self.parent.R, self.R, self.a, self.i)
        except ValueError:
            return np.nan

    def calcScaleHeight(self):
        raise NotImplementedError
        # return eq.scaleHeight(self.T, , self.g)  # TODO mu based on assumptions

    def calcTransitDepth(self):
        return eq.transitDepth(self.star.R, self.R)

    def type(self):
        return assum.planetType(self.T, self.M, self.R)

    def massType(self):
        return assum.planetMassType(self.M)

    def radiusType(self):
        return assum.planetRadiusType(self.R)

    def tempType(self):
        return assum.planetTempType(self.T)

    def mu(self):  # TODO make getter look in params first calc if not

        molweight = self.getParam('molweight')

        if molweight is np.nan:  # Use assumptions
            if self.M is not np.nan:
                return assum.planetMu(self.massType())
            elif self.R is not np.nan:
                return assum.planetMu(self.radiusType())
            else:
                return np.nan
        else:
            return molweight

    def albedo(self):
        if self.getParam('temperature') is not np.nan:
            planetClass = self.tempType()
        elif self.M is not np.nan:
            planetClass = self.massType()
        elif self.R is not np.nan:
            planetClass = self.radiusType()

        return assum.planetAlbedo(planetClass)

    def calcTemperature(self):
        """ Calculates the temperature using which uses equations.meanPlanetTemp, albedo assumption and potentially
        equations.starTemperature.

        issues
        - you cant get the albedo assumption without temp but you need it to calculate the temp.
        """
        try:
            return eq.meanPlanetTemp(self.albedo(), self.star.T, self.star.R, self.a)
        except ValueError:  # ie missing value (.a) returning nan
            return np.nan

    def estimateMass(self):

        density = assum.planetDensity(self.radiusType())

        return eq.estimateMass(self.R, density)

    def calcSMA(self):
        """ Calculates the semi-major axis based on star mass and period
        """

        return eq.calcSemiMajorAxis(self.P, self.star.M)

    def calcSMAfromT(self):
        """ Calculates the semi-major axis based on planet temperature
        """

        return eq.calcSemiMajorAxis2(self.T, self.star.T, self.albedo(), self.star.R)

    def calcPeriod(self):
        """ calculates period using a and stellar mass
        """

        return eq.calcPeriod(self.a, self.star.M)

    @property
    def discoveryMethod(self):
        return self.getParam('discoverymethod')

    @property
    def discoveryYear(self):
        return self.getParam('discoveryyear')

    @property
    def e(self):
        return self.getParam('eccentricity')

    @property
    def lastUpdate(self):
        return self.getParam('lastupdate')

    @property
    def i(self):
        return self.getParam('inclination')

    @property
    def P(self):
        period = self.getParam('period')
        if period is not np.nan:
            return period
        else:
            return self.calcPeriod()

    @property
    def a(self):

        sma = self.getParam('semimajoraxis')
        if sma is np.nan:
            if self.getParam('period') is np.nan:
                sma = self.calcSMAfromT()
            else:
                sma = self.calcSMA()  # calc using period
            self.flags.addFlag('Calculated SMA')

        return sma

    @property
    def transittime(self):
        return self.getParam('transittime')

    @property
    def star(self):
        return self.parent


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
            'age': aq.Gyear,
            'distance': pq.pc, # TODO more specific unit handling here or in classes?
            'magB': 1,
            'magH': 1,
            'magI': 1,
            'magJ': 1,
            'magK': 1,
            'magV': 1,
            'temperature': pq.K,
        }

        self.rejectTags = ('system', 'binary', 'star', 'planet', 'moon')  # These are handled in their own classes

    def addParam(self, key, value, attrib=None):
        """ Checks the key dosnt already exist, adds alternate names to a seperate list

        Future
            - format input and add units
            - logging
        """

        if key in self.rejectTags:
            return False  # TODO Replace with exception

        if key in self.params:  # if already exists

            if key == 'name':
                try:  # if flagged as a primary or popular name use this one, an option should be made to use either
                    if attrib['type'] == 'pri':  # first names or popular names.
                        oldname = self.params['name']
                        self.params['altnames'].append(oldname)
                        self.params['name'] = value
                    else:
                        self.params['altnames'].append(value)
                except (KeyError, TypeError):  # KeyError = no type key in attrib dict, TypeError = not a dict
                    self.params['altnames'].append(value)
            elif key == 'list':
                self.params['list'].append(value)
            else:
                try:
                    name = self.params['name']
                except KeyError:
                    name = 'Unnamed'
                print 'rejected duplicate {}: {} in {}'.format(key, value, name)  # TODO: log rejected value
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


class BinaryParameters(Parameters):

    def __init__(self):

        Parameters.__init__(self)

        self._defaultUnits.update({
         # TODO add binary parameters
        })


class StarParameters(Parameters):

    def __init__(self):

        Parameters.__init__(self)

        self._defaultUnits.update({
            'mass': aq.M_s,
            'metallicity': 1,
            'radius': aq.R_s,
        })


class PlanetParameters(Parameters):

    def __init__(self):

        Parameters.__init__(self)

        self._defaultUnits.update({
            'discoveryyear': 1,
            'mass': aq.M_j,
            'radius': aq.R_j,
            'inclination': pq.deg,
            'eccentricity': 1,
            'period': pq.day,
            'semimajoraxis': pq.au,
            'transittime': pq.d,
            'molweight': pq.atomic_mass_unit,
        })


def _findNearest(arr, value):
    """ Finds the value in arr that value is clostest to
    """
    arr = np.array(arr)
    # find nearest value in array
    idx = (abs(arr-value)).argmin()
    return arr[idx]


class SpectralType(object):
    """ Takes input of a spectral type as a string and interprets it into the luminosity class and stellar type.

    .. usage :
        self.lumType = Luminosity Class
        self.classLetter = Stellar Class (ie O B A etc)
        self.classNumber = Stellar Class number
        self.specClass = ie A8V will be A8
        self.specType = ie A*V will be A8V (default for calling the class)
        self.original = the original string

    This class ignores spaces, only considers the first class if given multiple options (ie K0/K1V, GIV/V, F8-G0)
    ignores non-typical star classes (ie ) and ignores extra statements like G8 V+
    """

    def __init__(self, classString):
        self.original = classString
        self.lumType = ''
        self.classLetter = ''
        self.classNumber = ''

        self._parseSpecType(classString)

    @property
    def specClass(self):
        """ Spectral class ie A8V is A8 """
        return self.classLetter + str(self.classNumber)

    @property
    def specType(self):
        """ Spectral class ie A8V is A8V """
        return self.classLetter + str(self.classNumber) + self.lumType

    def __repr__(self):
        return self.specType

    def _parseSpecType(self, classString):
        classString = str(classString)
        # some initial cases
        if classString == '' or classString == 'nan':
            return False
        #               main sequence
        possClasses = ('O', 'B', 'A', 'F', 'G', 'K', 'M',
                       'L', 'T', 'Y',  # dwarfs
                       'C', 'S',  # 'MS', 'MC' carbon related classes TODO handle multi letter classes
        )
        possNumbers = range(10)
        possLType = ('III', 'II', 'Iab', 'Ia0', 'Ia', 'Ib', 'IV', 'V')  # in order of unique matches

        # remove spaces, remove slashes
        classString = classString.replace(' ', '')

        classString = classString.replace('-', '/')
        classString = classString.replace('\\', '/')
        classString = classString.split('/')[0]

        # first char should always be spectral type
        stellarClass = classString[0]

        if stellarClass not in possClasses:
            return False  # assume a non standard class and fail
        else:
            self.classLetter = stellarClass

        # get number
        try:
            classNum = int(classString[1])
            if classNum in possNumbers:
                self.classNumber = int(classNum)
                typeString = classString[2:]
            else:
                return False  # invalid number received
        except IndexError:  # reached the end of the string
            return True
        except ValueError:  # i.e its a letter - fail # TODO multi letter checking
            typeString = classString[1:]

        if typeString == '':  # ie there is no more information as in 'A8'
            return True

        # Now check for a decimal and handle those cases
        if typeString[0] == '.':
            # handle decimal cases, we check each number in turn, add them as strings and then convert to float and add
            # to original number
            decimalNumbers = '.'
            for number in typeString[1:]:
                try:
                    if int(number) in possNumbers:
                        decimalNumbers += number
                    else:
                        print ('Something went wrong in decimal checking') # TODO replace with logging
                        return False # somethings gone wrong
                except ValueError:
                    break  # recevied a non-number (probably L class)
            #  add decimal to classNum
            try:
                self.classNumber += float(decimalNumbers)
            except ValueError: # probably trying to convert '.' to a float
                pass
            typeString = typeString[len(decimalNumbers):]
            if len(typeString) is 0:
                return True

        # Handle luminosity class
        for possL in possLType:  # match each possible case in turn (in order of uniqueness)
            Lcase = typeString[:len(possL)]  # match from front with length to minimise matching say IV in '<3 CIV'
            if possL == Lcase:
                self.lumType = possL
                return True

        if not self.classNumber == '':
            return True
        else:  # if there no number asumme we have a name ie 'Catac. var.'
            self.classLetter = ''
            self.classNumber = ''
            self.lumType = ''
            return False

_ExamplePlanetCount = 1  # Used by example.py - put here to enable global