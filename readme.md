# Open Exoplanet Catalogue Python

This python interface serves as a link between the raw XML of the [Open Exoplanet Catalogue](/hannorein/open_exoplanet_catalogue). It allows:
* Searching of planets (including alternate names)
* Easy reference of planet parameters ie GJ1214b.ra, GJ1214b.T, GJ1214b.R
* Calculation of values like the transit duration.
* Define planet types and query planets to find out what they are
* Easy rescale of units
* Easily navigate hierarchy (ie from planet to star or star to planets)
* Availability of system parameters in planets (ie ra, dec, d (distance))

Please note that this package is currently in Beta. The Docs are incomplete, it is not fully unit tested andany and all methods and variables are subjected the change in the development process

# Installation
This module depends on
* [Quantities](/python-quantities/python-quantities)
* numpy
* [Open Exoplanet Catalogue](/hannorein/open_exoplanet_catalogue) (somewhere on your system)

To install simply clone the repo and move into your python path. I have named the repo folder exoplanetcatalogue for ease. In future this package will be in a package manager which will avoid the naming issue.

# Usage

	import exoplanetcatalogue as oec # Note: exoplanetcatalogue should be your folder name of the repo
	databaseLocation = '/git/open-exoplanet-catalogue-atmospheres/systems/' # Your path here
	oecDB = oec.OECDatabase(databaseLocation)

You can then access the lists

	oecDB.systems
	oecDB.stars
	oecDB.planets
	oecDB.transitingPlanets

And perform more advanced queries such as fetching all planets whose radius is less than 10 Earth Radii
	
	superEarths = [planet for planet in oecDB.planets if planet.R < (10 * oec.R_e)]

To choose a planet

	kepler60b = oecDB.searchPlanet('kepler60b')
	kepler60planets = oecDB.searchPlanet('kepler60') # or all the kepler 60 planets
	kepler60 = kepler60b.star #to het the star kepler-60

	kepler60b.R # get planet radius

	>>> array(0.207777) * jupiter_radius # this works like an array in most functions
	kepler60b.R.rescale(oec.R_e) # See Units section for more
	>>> array(2.280002801287082) * earth_radius

	kepler60b.R.rescale(pq.m) # import quantities as pq (se units section)
	>>> array(14525897.847) * m

	kepler60b.RA
	>>> '20 02 28'

	gj1214.type()
	>>> 'Warm Super-Earth' # Note: This depends on your asumptions, see later

For a full list of planet, star and system parameters see [this wiki page](wiki/Planet,-Star-and-Systems-parameters-and-Methods)

# Units
units are handled by the quantities package
`import quantities as pq`

You can then access most units and constants such as meters pq.m, astronomical units pq.au etc!

Some astronomy units such as R_e, R_j, R_s (where e is Earth, j is Jupiter and s in the Sun) arent inlcuded (yet) in quantities so you need to refer to them as oec.R_e (or whatever you called this module on import)

There are also M_e, M_s, M_j.

Please read more about [Quantities](/python-quantities/python-quantities)

# Equations

The module contains several equations at the moment and i plan to add many more. If you want one why not write it and send me a pull request or open an issue.


	kepler60b.calcSurfaceGravity()
	>>> array(10.318715585166878) * m/s**2

	kepler60b.calcLogg()
	>>> 6.93912947949421

	gj1214.calcTansitDuration()
	array(54.73064331158644) * min

see [the docs](wiki/Planet,-Star-and-Systems-parameters-and-Methods) for a full list

# Assumptions

This is a hard module to make and i will open an issue on it soon. Currently they are stored in the dictionary exoplanetcatalogue.assumptions.planetAssumptions.

Overwriting these values (or adding new ones) will change the output.

Please see assumptions.py for how to do this.

# License

Copyright (C) 2013 Ryan Varley

Permission is hereby granted, free of charge, to any person obtaining a copy of this package to deal with the package without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Database, and to permit persons to whom the package is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the package. A reference to the package shall be included in all scientific publications that make use of the package.

THE PACKAGE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE PACKAGE OR THE USE OR OTHER DEALINGS IN THE PACKAGE.