# ExoData
[![Build Status](https://api.travis-ci.org/ryanvarley/ExoData.png?branch=master)](https://travis-ci.org/ryanvarley/ExoData)
[![Coverage Status](https://coveralls.io/repos/ryanvarley/ExoData/badge.svg)](https://coveralls.io/r/ryanvarley/ExoData)

This python interface (formerly oecpy) serves as a link between the raw XML of the [Open Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue). It allows:
* Searching of planets (including alternate names)
* Easy reference of planet parameters ie GJ1214b.ra, GJ1214b.T, GJ1214b.R
* Calculation of values like the transit duration.
* Define planet types and query planets to find out what they are
* Easy rescale of units
* Easily navigate hierarchy (ie from planet to star or star to planets)
* Availability of system parameters in planets (ie ra, dec, d (distance))

Please note that this package is in active development. The Docs are incomplete, it is not fully unit tested and any and all methods and variables are subject to change in the development process

# Installation
This module depends on
* [Quantities](https://github.com/python-quantities/python-quantities)
* [numpy](http://www.numpy.org/)
* nose
* matplotlib
* requests
* [Open Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue) (somewhere on your system)

**Currently only tested under Python 2.6, 2.7, 3.3, 3.4 on mac and linux**. If you use windows or a different python version try it anyway and open an issue if you encounter problems.

Easiest way

`pip install exodata`

Or from this repo

    python setup.py install

You can either download and manage the Open Exoplanet Catalogue yourself or automatically load the latest version from the web each time.

To get your own copy move to the folder on your system where you want to store it and clone the Open Exoplanet Catalogue (this process will create a folder named open-exoplanet-catalogue within your working directory).

    git clone https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue.git

The catalogue should then download. If you want to update the catalogue, move to the open_exoplanet_catalogue folder and pull

    cd open_exoplanet_catalogue/
    git pull origin master

If you want to keep track of this repo in a GUI way, I recommend [sourcetree](http://www.sourcetreeapp.com/) or the [github client](https://help.github.com/articles/set-up-git).

# Usage

	import exodata
	databaseLocation = '/git/open_exoplanet_catalogue/systems/' # Your path here (to systems folder)
	exocat = exodata.OECDatabase(databaseLocation)

	# To automatically load the latest version from github you can instead use load_db_from_url() which fetches
	# the latest version from https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz
	exocat = exodata.load_db_from_url()

You can then access the lists

	exocat.systems
	exocat.stars
	exocat.planets
	exocat.transitingPlanets

The following code assumes the imports

    import exodata
    import quantities as pq
    import exodata.astroquantities as aq

You can now perform more advanced queries such as fetching all planets whose radius is less than 10 Earth Radii

	superEarths = [planet for planet in exocat.planets if planet.R < (10 * aq.R_e)]

To choose a planet

	kepler60b = exocat.searchPlanet('kepler60b')
	>>> Planet('Kepler-60 b')
	kepler60planets = exocat.searchPlanet('kepler60') # or all the kepler 60 planets
	>>> [Planet('Kepler-60 c'), Planet('Kepler-60 b'), Planet('Kepler-60 d')]
	kepler60 = kepler60b.star #to get the star kepler-60
	>>> Star('Kepler-60')

	kepler60b.R # get planet radius
	>>> array(0.207777) * jupiter_radius # this works like an array in most functions

	kepler60b.R.rescale(aq.R_e) # See Units section for more
	>>> array(2.280002801287082) * earth_radius

	kepler60b.R.rescale(pq.m) # import quantities as pq (se units section)
	>>> array(14525897.847) * m

	kepler60b.RA
	>>> '20 02 28'

    gj1214 = exocat.searchPlanet('gj1214')
    # or with the exact name
    exocat.planetDict['Gliese 1214 b']
	gj1214.type()
	>>> 'Warm Super-Earth' # Note: This depends on your asumptions, see later

For a full list of planets, star and system parameters see COMING SOON

# Units
units are handled by the quantities package
`import quantities as pq`

You can then access most units and constants such as meters pq.m, astronomical units pq.au etc!

Some astronomy units such as R_e, R_j, R_s (where e is Earth, j is Jupiter and s in the Sun) are not included (yet) in quantities so you need to refer to them as aq.R_e by importing exodata.astroquantities as aq

There are also M_e, M_s, M_j.

Please read more about [Quantities](https://github.com/python-quantities/python-quantities)

# Equations

The module contains several equations at the moment and I plan to add many more. If you want one why not write it yourself and send me a pull request or open an issue with a request.


	kepler60b.calcSurfaceGravity()
	>>> array(10.318715585166878) * m/s**2

	kepler60b.calcLogg()
	>>> 6.93912947949421

	gj1214.calcTansitDuration()
	>>> array(54.73064331158644) * min

see COMING SOON

# Assumptions

Currently they are stored in the dictionary exoplanetcatalogue.assumptions.planetAssumptions.

Overwriting these values (or adding new ones) will change the output.

Please see assumptions.py for how to do this.

# OECPY Global Parameters
A few options can be set within OECPY to change the behaviour of the program. By default if a quantity is missing for a parameter it is calculated if possible. For example if you use .a for the semi-major axis and it is not present in the catalogue it will be calculated using the period and stellar mass and returned. this happens silently except for raising the `Calculated SMA` flag. (see flags). You can turn this behaviour off by typing

`exodata.params.estimateMissingValues = False`

This will only take scope in the current project so if you close the interpreter it will reset to True.

# Plotting
ExoData features a plotting library for planet and stellar parameters in a scatter plot and per parameter bin. Please see the [plots section](https://github.com/ryanvarley/open-exoplanet-catalogue-python/wiki/Plotting) of the documentation for further information.

### Planet Mass with Planet Radius ###
```python
exodata.plots.GeneralPlotter(exocat.planets, 'R', 'M', yaxislog=True).plot()
```
![Planet Mass with Planet Radius](https://raw.githubusercontent.com/ryanvarley/ExoData/images/exodata-planet-mass-radius.png "Planet Mass with Planet Radius Plot")

### Stellar V Magnitude with Planet Radius ###
```python
exodata.plots.GeneralPlotter(exocat.planets, 'R', 'star.magV',
                            xunit=aq.R_e, xaxislog=True).plot()
```

![Stellar V Magnitude with Planet Radius](https://raw.githubusercontent.com/ryanvarley/ExoData/images/exodata-vmag-planetradius.png "Stellar V Magnitude with Planet Radius Plot")

### Planet Eccentricity ###
```python
exodata.plots.DataPerParameterBin(exocat.planets, 'e',
      (0, 0, 0.05, 0.1, 0.2, 0.4, float('inf'))).plotBarChart(label_rotation=45)
```
![Planet Eccentricity](https://raw.githubusercontent.com/ryanvarley/ExoData/images/exodata-orbital-eccentricity-3.png "Planet Eccentricity Plot")

You can also plot this as a pie chart

```python
exodata.plots.DataPerParameterBin(exocat.planets, 'e',
      (0, 0, 0.05, 0.1, 0.2, 0.4, float('inf'))).plotPieChart)
```

![Planet Eccentricity](https://raw.githubusercontent.com/ryanvarley/ExoData/images/exodata-orbital-eccentricity-pie.png "Planet Eccentricity Pie Chart")

Plots can also be large (i.e. for presentations), and you can change the color easily with normal *matplotlib* syntax

```python
exodata.plots.DataPerParameterBin(exocat.planets, 'M',
    (0, 0.2, 0.5, 1, 2, 3, 6, 12, float('inf')), size='large').plotBarChart(c='r')
```
![Planet Eccentricity](https://raw.githubusercontent.com/ryanvarley/ExoData/images/exodata-orbital-eccentricity-large-2.png "Planet Eccentricity Plot Large")

# Licence

Copyright (C) 2013  Ryan Varley <ryanjvarley@gmail.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
