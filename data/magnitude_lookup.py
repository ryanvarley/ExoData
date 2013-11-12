""" Rather than reformat everything in python code, it is much easier just to do it here.

Table has been taken from http://www.uni.edu/morgans/astro/course/Notes/section2/spectraltemps.html on 12/11/2013
"""

from collections import OrderedDict

mag_lookup_dict = OrderedDict({
    'O': OrderedDict({5: -4.5, 6: -4, 7: -3.9, 8: -3.8, 9: -3.6}),
    'B': OrderedDict({0: -3.3, 1: -2.3, 2: -1.9, 3: -1.1, 5: -0.4, 6: 0, 7: 0.3, 8: 0.7, 9: 1.1}),
    'A': OrderedDict({0: 1.5, 1: 1.7, 2: 1.8, 3: 2.0, 4: 2.1, 5: 2.2, 7: 2.4}),
    'F': OrderedDict({0: 3.0, 2: 3.3, 3: 3.5, 5: 3.7, 6: 4, 7: 4.3, 8: 4.4}),
    'G': OrderedDict({0: 4.7, 1: 4.9, 2: 5.0, 5: 5.2, 8: 5.6}),
    'K': OrderedDict({0: 6, 1: 6.2, 2: 6.4, 3: 6.7, 4: 7.1, 5: 7.4, 7: 8.1}),
    'M': OrderedDict({0: 8.7, 1: 9.4, 2: 10.1, 3: 10.7, 4: 11.2, 5: 12.3, 6: 13.4, 7: 13.9}),
})