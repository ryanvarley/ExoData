""" This module contains some plotting functions and plot types for easy plot creation
"""

from collections import OrderedDict
import os
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams, ticker
from matplotlib.ticker import ScalarFormatter

rcParams.update({'figure.autolayout': True})


class GlobalFigure(object):
    """ sets up the figure and subfigure object with all the global parameters.
    """

    def __init__(self):
        self.setup_fig()

    def setup_fig(self):
        self.fig = fig = plt.figure(figsize=(5, 4))
        self.ax = fig.add_subplot(1, 1, 1)

        # initial fonts and colours
        self.set_title_size(10)
        self.set_axis_label_size(12)
        self.set_axis_tick_label_size(12)

    def set_global_font_size(self, fontsize):
        ax = self.ax
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(fontsize)
        plt.draw()

    def set_title_size(self, fontsize):
        self.ax.title.set_fontsize(fontsize)
        plt.draw()

    def set_axis_label_size(self, fontsize):
        for axis in (self.ax.xaxis.label, self.ax.yaxis.label):
            axis.set_fontsize(fontsize)
        plt.draw()

    def set_axis_tick_label_size(self, fontsize):
        for axis in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            axis.set_fontsize(fontsize)
        plt.draw()

    # set_foregroundcolor / set_backgroundcolor from Jasonmc https://gist.github.com/jasonmc/1160951
    def set_foregroundcolor(self, color):
         '''For the specified axes, sets the color of the frame, major ticks,
             tick labels, axis labels, title and legend
         '''

         ax = self.ax

         for tl in ax.get_xticklines() + ax.get_yticklines():
             tl.set_color(color)
         for spine in ax.spines:
             ax.spines[spine].set_edgecolor(color)
         for tick in ax.xaxis.get_major_ticks():
             tick.label1.set_color(color)
         for tick in ax.yaxis.get_major_ticks():
             tick.label1.set_color(color)
         ax.axes.xaxis.label.set_color(color)
         ax.axes.yaxis.label.set_color(color)
         ax.axes.xaxis.get_offset_text().set_color(color)
         ax.axes.yaxis.get_offset_text().set_color(color)
         ax.axes.title.set_color(color)
         lh = ax.get_legend()
         if lh != None:
             lh.get_title().set_color(color)
             lh.legendPatch.set_edgecolor('none')
             labels = lh.get_texts()
             for lab in labels:
                 lab.set_color(color)
         for tl in ax.get_xticklabels():
             tl.set_color(color)
         for tl in ax.get_yticklabels():
             tl.set_color(color)
         plt.draw()

    def set_backgroundcolor(self, color):
         '''Sets the background color of the current axes (and legend).
             Use 'None' (with quotes) for transparent. To get transparent
             background on saved figures, use:
             pp.savefig("fig1.svg", transparent=True)
         '''
         ax = self.ax
         ax.patch.set_facecolor(color)
         lh = ax.get_legend()
         if lh != None:
             lh.legendPatch.set_facecolor(color)

         plt.draw()


class BaseDataPerClass(GlobalFigure):
    """ Base class for plots counting the results by a attribute. Child classes must modify
    * _classVariables (self._allowedKeys, )
    * _getSortKey (take the planet, turn it into a key)
    """

    def __init__(self, astroObjectList):
        GlobalFigure.__init__(self)
        self._classVariables()  # add info from child classes
        self.astroObjectList = astroObjectList
        self.resultsByClass = self._processResults()

    def _classVariables(self):
        """ Variables to be loaded in init by child classes

        must set
        *self._allowedKeys = (tuple of keys)
        """
        self._allowedKeys = ('Class')

    def _getSortKey(self, planet):
        """ Takes a planet and turns it into a key to be sorted by
        :param planet:
        :return:
        """

        return 'Class'

    def _processResults(self):
        """ Checks each result can meet SNR requirments, adds to count
        :return:
        """

        resultsByClass = self._genEmptyResults()

        for astroObject in self.astroObjectList:
            sortKey = self._getSortKey(astroObject)
            resultsByClass[sortKey] += 1

        return resultsByClass

    def plotBarChart(self, title='', xlabel='', c='#3ea0e4', xticksize=8, rotation=False):
        resultsByClass = self.resultsByClass

        self.setup_fig()
        ax = self.ax

        try:
            if resultsByClass['Uncertain'] == 0:  # remove uncertain tag if present and = 0
                resultsByClass.pop('Uncertain', None)
        except KeyError:
            pass

        plotData = zip(*resultsByClass.items())

        ydata = plotData[1]

        numItems = float(len(ydata))

        ind = np.arange(numItems)  # the x locations for the groups
        ind /= numItems # between 0 and 1

        spacePerBar = 1./numItems
        gapratio = 0.5 # gap to bar ratio, 0.5 is even
        width = spacePerBar*gapratio
        gap = spacePerBar - width

        ax.bar(ind, plotData[1], width, color=c)
        ax.set_xticklabels(plotData[0])
        ax.set_xticks(ind+(width/2.))

        for axis in self.ax.get_xticklabels():
            axis.set_fontsize(xticksize)

        if rotation:
            plt.xticks(rotation=rotation)
        plt.ylabel('Number of Observable Planets')
        plt.xlabel(xlabel)
        plt.title(title)
        plt.xlim([min(ind)-gap, max(ind)+(gap*2)])
        plt.draw()

    def saveAllBarChart(self, filepath, *args, **kwargs):
        self.plotBarChart(*args, **kwargs)
        plt.savefig(os.path.join(filepath))

    def _genEmptyResults(self):
        """ Uses allowed keys to generate a empty dict to start counting from
        :return:
        """

        allowedKeys = self._allowedKeys

        keysDict = OrderedDict()  # Note: list comprehension take 0 then 2 then 1 then 3 etc for some reason. we want strict order
        for k in allowedKeys:
            keysDict[k] = 0


        resultsByClass = keysDict

        return resultsByClass


class DataPerParameterBin(BaseDataPerClass):
    """ Generates Data for observable planets per parameter bin"""

    def __init__(self, results, planetProperty, binLimits):
        """
        :param planetProperty: property of planet to bin. IE 'e' for eccentricity, 'parent.magV' for magV
        :param binLimits: list of bin limits (lower limit, upper, upper, maximum) (note you can have maximum +)
        :return:
        """

        self._binlimits = binLimits
        self._planetProperty = planetProperty

        self._genKeysBins()  # Generate the bin keys/labels (must do before base class processes results)
        BaseDataPerClass.__init__(self, results)

    def _getSortKey(self, planet):
        """ Takes a planet and turns it into a key to be sorted by
        :param planet:
        :return:
        """

        value = eval('planet.'+self._planetProperty)

        # TODO some sort of data validation, either before or using try except

        return sortValueIntoGroup(self._allowedKeys[:-1], self._binlimits, value)

    def _classVariables(self):
        pass  # Overload as we dont want it to set anything in this class

    def _genKeysBins(self):
        """ Generates keys from bins, sets self._allowedKeys normally set in _classVariables
        """
        binlimits = self._binlimits

        allowedKeys = []
        midbinlimits = binlimits

        if binlimits[0] == -float('inf'):
            midbinlimits = binlimits[1:]  # remove the bottom limit
            allowedKeys.append('<{}'.format(midbinlimits[0]))

        if binlimits[-1] == float('inf'):
            midbinlimits = midbinlimits[:-1]

        lastbin = midbinlimits[0]

        for binlimit in midbinlimits[1:]:
            if lastbin == binlimit:
                allowedKeys.append('{}'.format(binlimit))
            else:
                allowedKeys.append('{} to {}'.format(lastbin, binlimit))
            lastbin = binlimit

        if binlimits[-1] == float('inf'):
            allowedKeys.append('{}+'.format(binlimits[-2]))

        allowedKeys.append('Uncertain')
        self._allowedKeys = allowedKeys


class GeneralPlotter(GlobalFigure):
    """ This class should be able to create a plot with lots of options like the online visual plots. In future it
    should be turned into a GUI
    """

    def __init__(self, objectList, xaxis=None, yaxis=None):
        """
        :param objectList: list of astro objects to use in plot ie planets, stars etc
        :param xaxis: value to use on the xaxis, should be a variable or function of the objects in objectList. ie 'R'
            for the radius variable and 'calcDensity()' for the calcDensity function
        :param yaxis: value to use on the yaxis, should be a variable or function of the objects in objectList. ie 'R'
            for the radius variable and 'calcDensity()' for the calcDensity function

        :type objectList: list, tuple
        :type xaxis: str
        :type yaxis: str
        """
        GlobalFigure.__init__(self)

        self.objectList = objectList  # list of planets, stars etc

        if xaxis:
            self.set_xaxis(xaxis)
        else:
            self.xaxis = None

        if yaxis:
            self.set_yaxis(yaxis)
        else:
            self.yaxis = None

    def plot(self):
        xaxis = self.xaxis
        yaxis = self.yaxis

        assert(len(xaxis) == len(yaxis))

        plt.scatter(xaxis, yaxis)

    def _set_axis(self, param):
        """ this should take a variable or a function and turn it into a list by evaluating on each planet
        """
        return [eval('astroObject.{}'.format(param)) for astroObject in self.objectList]

    def set_xaxis(self, param):
        """ Sets the value of use on the x axis
        :param param: value to use on the xaxis, should be a variable or function of the objects in objectList. ie 'R'
        for the radius variable and 'calcDensity()' for the calcDensity function
        """
        self.xaxis = self._set_axis(param)

    def set_yaxis(self, param):
        """ Sets the value of use on the yaxis
        :param param: value to use on the yaxis, should be a variable or function of the objects in objectList. ie 'R'
        for the radius variable and 'calcDensity()' for the calcDensity function
        """
        self.yaxis = self._set_axis(param)

    def set_y_axis_log(self, logscale=True):
        # TODO write code and include code to modify labels
        pass

    def set_x_axis_log(self, logscale=True):
        pass

    def set_marker_color(self):
        # TODO allow a single colour or colour set per another variable
        pass


def sortValueIntoGroup(groupKeys, groupLimits, value):
    """ returns the Key of the group a value belongs to
    :param groupKeys: a list/tuple of keys ie ['1-3', '3-5', '5-8', '8-10', '10+']
    :param groupLimits: a list of the limits for the group [1,3,5,8,10,float('inf')] note the first value is an absolute
    minimum and the last an absolute maximum. You can therefore use float('inf')
    :param value:
    :return:
    """

    if not len(groupKeys) == len(groupLimits)-1:
        raise ValueError('len(groupKeys) must equal len(grouplimits)-1 got \nkeys:{} \nlimits:{}'.format(groupKeys,
                                                                                                         groupLimits))

    if value is np.nan:
        return 'Uncertain'

    # TODO add to other if bad value or outside limits
    keyIndex = None

    if value == groupLimits[0]:  # if value is == minimum skip the comparison
        keyIndex = 1
    elif value == groupLimits[-1]:  # if value is == minimum skip the comparison
        keyIndex = len(groupLimits)-1
    else:
        for i, limit in enumerate(groupLimits):
            if value < limit:
                keyIndex = i
                break

    if keyIndex == 0:  # below the minimum
        raise BelowLimitsError('Value {} below limit {}'.format(value, groupLimits[0]))

    if keyIndex is None:
        raise AboveLimitsError('Value {} above limit {}'.format(value, groupLimits[-1]))

    return groupKeys[keyIndex-1]


class OutOfLimitsError(Exception):
    pass


class BelowLimitsError(Exception):
    pass


class AboveLimitsError(Exception):
    pass