Introduction
============

This python interface serves as a link between the raw XML of the
 `Open Exoplanet Catalogue <https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue>`_.
 It allows:

* Searching of planets (including alternate names)
* Easy reference of planet parameters ie GJ1214b.ra, GJ1214b.T, GJ1214b.R
* Calculation of values like the transit duration.
* Define planet types and query planets to find out what they are
* Easy rescale of units
* Easily navigate hierarchy (ie from planet to star or star to planets)
* Availability of system parameters in planets (ie ra, dec, d (distance))

If you use ExoData in a scientific publication, please include a reference to
this paper `2015arXiv151002738V <http://arxiv.org/abs/1510.02738>`_.

Installation
------------

Install ExoData by running:

    pip install exodata

Or download the `repo <https://github.com/ryanvarley/ExoData>`_ and run

	python setup.py install


Getting Started
---------------

These docs are a work in progress and quite incomplete. The best place to start
at present is the readme on the project
`github page <https://github.com/ryanvarley/ExoData/blob/master/readme.md>`_.
If you want more information the `paper <http://arxiv.org/abs/1510.02738>`_
gives some more information and examples.


Modules
-------
ExoData is split into a series of modules dealing with the exoplanet database,
equations, plots and units.

+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Module          | Description                                                                                                                                         |
+=================+=====================================================================================================================================================+
| Assumptions     | Holds classification assumptions such as at what mass or radius a planet is defined as a super-Earth.                                               |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Astroclasses    | Classes for the System, Binary, Star and Planet object types.                                                                                       |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Astroquantities | Expands the *Product Quantities* Python package with astronomical units like Solar Radius and compound units such as :math:`g/cm^3`.                |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Database        | Holds the database class and the various search methods.                                                                                            |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Equations       | Implementation of exoplanet related equations including orbital equations, planet and star characterisations and estimations.                       |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Example         | Generate example systems for testing code.                                                                                                          |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Flags           | Each object has a flag object attached which lets you know which assumptions have been made such as "calculated temperature".                       |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+
| Plots           | Plot functions for common plot types that can be used to to easily display data from the catalogue.                                                 |
+-----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------+

Contents
--------

.. toctree::
   :maxdepth: 2

   index
   equations


License
-------

The project is licensed under the MIT license.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

