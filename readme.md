# Open Exoplanet Catalogue Python

This python interface serves as a link between the raw XML of the [Open Exoplanet Catalogue](https://github.com/hannorein/open_exoplanet_catalogue). It allows:
* Searching of planets (including alternate names)
* Easy reference of planet parameters ie GJ1214b.ra, GJ1214b.T, GJ1214b.R
* Calculation of values like the transit duration.
* Define planet types and query planets to find out what they are
* Easy rescale of units
* Easily navigate hierarchy (ie from planet to star or star to planets)
* Availability of system parameters in planets (ie ra, dec, d (distance))

Please note that this package is currently in Beta. The Docs are incomplete, it is not fully unit tested and any and all methods and variables are subjected to change in the development process

# Installation
This module depends on
* [Quantities](https://github.com/python-quantities/python-quantities)
* [numpy](http://www.numpy.org/)
* [Open Exoplanet Catalogue](https://github.com/hannorein/open_exoplanet_catalogue) (somewhere on your system)

**Currently only tested under Python 2.7 on mac**. If you use a different OS or python version try it anyway and open an issue if you encounter problems. Linux should be fine but windows may have some issues.

Easiest way

`pip install oecpy --pre` (currently in beta, --pre lets you grab it anyway)

Or from this repo

    python setup.py install

Now if you want to work with planets you need the exoplanet catalogue. Move to the folder on your system where you want to store it and clone the Open Exoplanet Catalogue

    git clone git@github.com:hannorein/open_exoplanet_catalogue.git

The catalogue should then download. If you want to update the catalogue, move to the open_exoplanet_catalogue folder and pull

    cd open_exoplanet_catalogue/
    git pull origin master

If you want to keep track of this repo in a GUI way, i recommend [sourcetree](http://www.sourcetreeapp.com/) or the [github client](https://help.github.com/articles/set-up-git).

# Usage

	import oecpy
	databaseLocation = '/git/open_exoplanet_catalogue/systems/' # Your path here (to systems folder)
	exocat = oecpy.OECDatabase(databaseLocation)

You can then access the lists

	exocat.systems
	exocat.stars
	exocat.planets
	exocat.transitingPlanets

The following code assumes the imports

    import oecpy
    import quantities as pq
    import oecpy.astroquantities as aq

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

Some astronomy units such as R_e, R_j, R_s (where e is Earth, j is Jupiter and s in the Sun) are not included (yet) in quantities so you need to refer to them as aq.R_e by importing oecpy.astroquantities as aq

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

# Licence

Copyright (C) 2013  Ryan Varley <ryanjvarley@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
