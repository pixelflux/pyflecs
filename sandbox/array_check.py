"""
A script to test how to dynamically create a numpy structured array.
"""

import numpy as np

import pyflecs as flecs

values = np.array([1, 2, 3], dtype='uint32')

flecs.test(values)
