"""
This provides a test to ensure numpy structured arrays
work as expected
"""
import numpy as np
import flecs


def test_structured_array():
    """
    Tests numpy structured arrays.
    """
    # Create a structured array
    array = np.array([1, 2, 3], dtype=[('a', 'uint32'), ('b', 'float'),
                                       ('c', 'uint8')])

    world = flecs.World()
    e = world.entity()
    c = world.component_from_example("test", array)

    e.set(c, array)

    result = e.get(c)

    np.testing.assert_array_equal(result, array)