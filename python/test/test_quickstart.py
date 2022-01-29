"""
This provides a test which runs through the quickstart
"""
import numpy as np
import pyflecs as flecs


def test_quickstart():
    world = flecs.world()

    e = world.entity()
    assert e.is_alive()
    e.destruct()
    assert not e.is_alive()

    e = world.entity("Bob")
    assert e.name() == "Bob"

    e = world.lookup("Bob")
    assert e.name() == "Bob"

    pos = np.array([1, 4, 2], dtype='uint8')
    position = world.component("Position", pos.nbytes, pos.dtype.alignment)

    e.add(position)
    e.set(position, pos)
    value = e.get(position)

    np.testing.assert_array_equal(value, pos)

    e.remove(position)
