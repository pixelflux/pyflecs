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


def test_bulk_prefab():
    """
    Creates a large number of entities using a prefab.
    """
    world = flecs.World()

    prefab = world.prefab()
    position = world.component("Position", 'float32', 3)
    velocity = world.component("Velocity", 'float32', 3)

    prefab.set(position, np.array([1, 2, 3], dtype='float32'))
    prefab.set(velocity, np.array([4, 5, 6], dtype='float32'))

    pair = world.pair(world.isa_entity, prefab)
    results = world.bulk_entity_w_id(pair, 1000)

    expr = 'Position, Velocity'
    query = world.query_builder(expr=expr, instanced=True).build()

    for val in query:
        assert len(val) == 1000
        # Just references
        assert len(val["Position"]) == 1
        assert len(val["Velocity"]) == 1


def test_bulk_create():
    """
    Creates from bulk components
    """
    world = flecs.World()
    rng = np.random.default_rng(12)

    position = world.component("Position", 'float32', 3)
    velocity = world.component("Velocity", 'float32', 3)

    position_data = rng.normal(size=(1000, 3)).astype('float32')
    velocity_data = rng.normal(size=(1000, 3)).astype('float32')

    bulk_builder = world.bulk_entity_builder(1000)
    bulk_builder.add(position, position_data)
    bulk_builder.add(velocity, velocity_data)
    entities = bulk_builder.build()

    expr = 'Position, Velocity'
    query = world.query_builder(expr=expr, instanced=True).build()

    for val in query:
        assert len(val) == 1000
        # Just references
        assert len(val["Position"]) == 1000
        assert len(val["Velocity"]) == 1000

        np.testing.assert_array_equal(val["Position"], position_data)


def test_hierarchy_cascade_simple():
    """
    This tests the cascade modifier in-use with the hierarchy.
    """
    world = flecs.World()
    position = world.component("Position", 'float32', 2)

    # Create out of order to show cascade working
    # Level 2
    moon = world.entity("Moon")
    moon.add(position)
    moon.set(position, np.array([1, 1], dtype='float32'))

    # Level 0
    sun = world.entity("Sun")
    sun.add(position)
    sun.set(position, np.array([1, 1], dtype='float32'))

    # Level 1
    mercury = world.entity("Mercury")
    sun.add_child(mercury)
    mercury.add(position)
    mercury.set(position, np.array([1, 1], dtype='float32'))

    venus = world.entity("Venus")
    sun.add_child(venus)
    venus.add(position)
    venus.set(position, np.array([2, 2], dtype='float32'))

    earth = world.entity("Earth")
    sun.add_child(earth)
    earth.add(position)
    earth.set(position, np.array([3, 3], dtype='float32'))

    # Level 2
    earth.add_child(moon)

    satellite = world.entity("Satellite")
    earth.add_child(satellite)
    satellite.add(position)
    satellite.set(position, np.array([2, 2], dtype='float32'))

    # Validate the paths
    assert sun.path == 'Sun'
    assert mercury.path == 'Sun.Mercury'
    assert venus.path == 'Sun.Venus'
    assert earth.path == 'Sun.Earth'
    assert moon.path == 'Sun.Earth.Moon'

    expr = 'Position, ?Position(parent|cascade)'
    query = world.query_builder(expr=expr, instanced=True).build()

    print(sun.type)
    print(earth.type)
    print(moon.type)

    # Store the number of iterations
    num_iter = 0
    for result in query:
        print(f"Iteration: {num_iter + 1}")
        for entity in result.entities:
            print(f"Entity: {entity.name}")
        print(result.term_count)
        print(f"Result[0] length: {len(result[0])}")
        print(f"Result[1] length: {len(result[1])}")
        print(f"Result[0]: {result[0]}")
        print(f"Result[1]: {result[1]}")
        num_iter += 1

    assert num_iter == 3


def test_hierarchy_cascade():
    """
    This tests the cascade modifier in-use with the hierarchy.
    """
    world = flecs.World()
    position = world.component("Position", 'float32', 2)
    local_coord = world.tag('Local')
    world_coord = world.tag('World')

    # Create the moon out of order to ensure cascade works
    moon = world.entity("Moon")
    moon.add_pair(position, world_coord)
    moon.set_pair(position, local_coord, np.array([1, 1], dtype='float32'))

    # Level 0
    sun = world.entity("Sun")
    sun.add_pair(position, world_coord)
    sun.set_pair(position, local_coord, np.array([1, 1], dtype='float32'))

    # Level 1
    mercury = world.entity("Mercury")
    sun.add_child(mercury)
    mercury.add_pair(position, world_coord)
    mercury.set_pair(position, local_coord, np.array([1, 1], dtype='float32'))

    venus = world.entity("Venus")
    sun.add_child(venus)
    venus.add_pair(position, world_coord)
    venus.set_pair(position, local_coord, np.array([2, 2], dtype='float32'))

    earth = world.entity("Earth")
    sun.add_child(earth)
    earth.add_pair(position, world_coord)
    earth.set_pair(position, local_coord, np.array([3, 3], dtype='float32'))

    # Level 2
    earth.add_child(moon)

    # Validate the paths
    assert sun.path == 'Sun'
    assert mercury.path == 'Sun.Mercury'
    assert venus.path == 'Sun.Venus'
    assert earth.path == 'Sun.Earth'
    assert moon.path == 'Sun.Earth.Moon'

    expr = '[in](Position,Local), [out](Position,World), ' \
           '[in]?Position(parent|cascade,World)'
    query = world.query_builder(expr=expr, instanced=True).build()

    # Store the number of iterations
    num_iter = 0
    for result in query:
        print(f"Iteration: {num_iter + 1}")
        for entity in result.entities:
            print(f"Entity: {entity.name}")
            print(f"Entity type: {entity.type}")
        print(f"Result[0] length: {len(result[0])}")
        print(f"Result[1] length: {len(result[1])}")
        print(f"Result[2] length: {len(result[2])}")
        print(f"Result[0]: {result[0]}")
        print(f"Result[1]: {result[1]}")
        print(f"Result[2]: {result[2]}")
        num_iter += 1
        if len(result[2]) > 0:
            result[1][:] = result[0] + result[2]
        else:
            result[1][:] = result[0]

    assert num_iter == 3






