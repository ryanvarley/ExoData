ExoData
=======

This python interface serves as a link between the raw XML of the `Open Exoplanet Catalogue <https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue>`_. It allows:
* Searching of planets (including alternate names)
* Easy reference of planet parameters ie GJ1214b.ra, GJ1214b.T, GJ1214b.R
* Calculation of values like the transit duration.
* Define planet types and query planets to find out what they are
* Easy rescale of units
* Easily navigate hierarchy (ie from planet to star or star to planets)
* Availability of system parameters in planets (ie ra, dec, d (distance))

If you use ExoData in a scientific publication, please include a reference to this paper `2015arXiv151002738V <http://arxiv.org/abs/1510.02738>`_.

# Installation
This module depends on
* `Quantities <https://github.com/python-quantities/python-quantities>`_
* `numpy <http://www.numpy.org/>`_
* nose
* matplotlib
* requests
* hypothesis
* seaborn
* `Open Exoplanet Catalogue <https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue>`_ (somewhere on your system)

Contents
--------

.. toctree::
   :maxdepth: 2

Installation
------------

Install ExoData by running:

    pip install exodata

Or download the `repo <https://github.com/ryanvarley/ExoData>`_ and run

	python setup.py install

Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/$project/$project

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@google-groups.com

License
-------

The project is licensed under the MIT license.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

