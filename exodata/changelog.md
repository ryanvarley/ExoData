Changelog
---

## 2.0

- Equations in equations module are now classes that are initialised with n-1 variables and will output the remaining
 one when called (as a variable of the class)
- Many unittests now include [hypothesis](http://hypothesis.readthedocs.org/en/latest/) for property based testing
- Dropped python 2.6 support. If you need to upgrade try [anaconda](http://continuum.io/downloads) or
 [miniconda](http://conda.pydata.org/miniconda.html)