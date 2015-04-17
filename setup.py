from setuptools import setup
import codecs
import os
import re
import sys
import multiprocessing  # stops exit fail on setup.py test

kw = {}
if sys.hexversion >= 0x03000000:
    kw['use_2to3'] = True

here = os.path.abspath(os.path.dirname(__file__))


# Read the version number from a source file.
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = ['numpy', 'quantities', 'nose>=1.0', 'matplotlib>=1.3.1', 'requests']
if sys.hexversion < 0x02070000:
    install_requires.append('unittest2')
    install_requires.append('ordereddict')

if sys.hexversion < 0x02070000:
    test_suite = 'exodata.tests.testsuite'  # otherwise skiptests dont work with 2.6, TODO plugin?
else:
    test_suite = 'nose.collector'


setup(
    name="exodata",
    version=find_version('exodata', '__init__.py'),
    description="Exoplanet catalogue interface",
    long_description=long_description,
    url='https://github.com/ryanvarley/exodata',
    author='Ryan Varley',
    author_email='oecpy@ryanvarley.uk',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.6',
    ],

    # What does your project relate to?
    # keywords='sample setuptools development',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=['exodata'],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed.
    install_requires = install_requires,

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data=True,
    zip_safe=False,
    test_suite = test_suite,

    **kw
)
