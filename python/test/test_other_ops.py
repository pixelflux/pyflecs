"""
Tests various other operations needed.
"""

import numpy as np
import flecs


def test_entity_w_id():
    """
    Tests that an entity can be created with a component.
    """
    world = flecs.World()

    # Define three components
    position = world.component("Position", 'float32', 3)

    e = world.entity(position)

    assert e.has(position)


def test_prefab():
    """
    Tests that prefab works as expected.
    """
    world = flecs.World()

    prefab = world.prefab()
    position = world.component("Position", 'float32', 3)
    velocity = world.component("Velocity", 'float32', 3)

    prefab.add(position)
    prefab.add(velocity)

    e = world.entity()
    e.is_a(prefab)

    assert e.has(position)
    assert e.has(velocity)
    assert not e.has(prefab)


def test_hierarchy_cascade():
    """
    This tests the cascade modifier in-use with the hierarchy.
    """
    world = flecs.World()
    position = world.component("Position", 'float32', 2)
    local_coord = world.tag('Local')
    world_coord = world.tag('World')

    # Level 0
    sun = world.entity()
    sun.add_pair(position, world_coord)
    sun.add_pair(position, local_coord)
    sun.set_pair(position, local_coord, np.array([1, 1], dtype='float32'))

    # Level 1
    mercury = world.entity()
    sun.add_child(mercury)
    mercury.add_pair(position, world_coord)
    mercury.add_pair(position, local_coord)
    mercury.set_pair(position, local_coord, np.array([1, 1], dtype='float32'))

    venus = world.entity()
    sun.add_child(venus)
    venus.add_pair(position, world_coord)
    venus.add_pair(position, local_coord)
    venus.set_pair(position, local_coord, np.array([2, 2], dtype='float32'))

    earth = world.entity()
    sun.add_child(earth)
    earth.add_pair(position, world_coord)
    earth.add_pair(position, local_coord)
    earth.set_pair(position, local_coord, np.array([3, 3], dtype='float32'))

    # Level 2
    moon = world.entity()
    earth.add_child(moon)
    moon.add_pair(position, world_coord)
    moon.add_pair(position, local_coord)
    moon.set_pair(position, local_coord, np.array([1, 1], dtype='float32'))

    expr = 'Position(Local)'
    query = world.query_builder(expr=expr).build()

    # Store the number of iterations
    num_iter = 0
    for result in query:
        print(result.term_count)
        num_iter += 1

    assert num_iter == 2






