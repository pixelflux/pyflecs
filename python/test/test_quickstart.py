"""
This provides a test which runs through the quickstart
"""
import numpy as np
import flecs


def test_quickstart():
    world = flecs.World()

    e = world.entity()
    assert e.is_alive
    e.destruct()
    assert not e.is_alive

    e = world.entity("Bob")
    assert e.name == "Bob"

    e2 = world.lookup("Bob")
    assert e2.name == "Bob"
    assert int(e2) == int(e)
    assert e2 == e

    # Lookup invalid name
    e3 = world.lookup("Something")
    assert e3 is None

    pos = np.array([1, 4, 2], dtype='float32')
    position = world.component("Position", pos.dtype, pos.shape)

    e.add(position)
    e.set(position, pos)
    value = e.get(position)
    np.testing.assert_array_equal(value, pos)

    # Retrieve position another way:
    position2 = world.lookup("Position")
    assert position2.is_component
    value2 = e.get(position2)
    np.testing.assert_array_equal(value2, pos)

    # Update the value
    value += [5, 1, 4]
    value = e.get(position)
    np.testing.assert_array_equal(value, pos + [5, 1, 4])

    assert e.has(position)
    e.remove(position)
    assert not e.has(position)

    # Create a tag
    enemy = world.tag("Enemy")
    e.add(enemy)
    assert e.has(enemy)
    e.remove(enemy)
    assert not e.has(enemy)

    # Option 2: use an entity
    friend = world.entity("Friend")
    e.add(friend)
    assert e.has(friend)
    e.remove(friend)
    assert not e.has(friend)

    # Create a Likes relation
    likes = world.tag("Likes")
    bob = world.lookup("Bob")
    alice = world.entity("Alice")
    bob.add_pair(likes, alice)
    assert not alice.has_pair(likes, bob)
    alice.add_pair(likes, bob)

    assert bob.has_pair(likes, alice)
    assert alice.has_pair(likes, bob)

    bob.remove_pair(likes, alice)
    assert not bob.has_pair(likes, alice)


def test_hierarchy():
    world = flecs.World()

    # Hierarchy
    parent = world.entity("parent")
    child = world.entity("child")

    parent.add_child(child)

    assert parent.path == 'parent'
    assert child.path == 'parent.child'

    child2 = parent.lookup('child')
    child3 = world.lookup_path('parent.child')
    assert child == child2
    assert child == child3

    # Destroy the parent
    assert parent.is_alive
    assert child.is_alive
    parent.destruct()
    assert not parent.is_alive
    assert not child.is_alive


def test_inheritance():
    """
    Tests that inheritance works
    """
    world = flecs.World()

    base = world.entity()
    triangle_data = np.array([[0, 0], [1, 1], [-1, -1]])
    triangle = world.component_from_example("Triangle", triangle_data)
    base.set(triangle, triangle_data)

    subclass = world.entity()
    subclass.is_a(base)

    data = subclass.get(triangle)

    np.testing.assert_array_equal(data, triangle_data)


def test_type():
    """
    Tests that the type string works as expected.
    """
    world = flecs.World()
    e = world.entity()
    position = world.tag("Position")
    velocity = world.tag("Velocity")
    e.add(position)
    e.add(velocity)

    assert e.type == 'Position, Velocity'


def test_filter():
    """
    Tests that the filter works.
    """
    world = flecs.World()
    e = world.entity()
    e2 = world.entity()
    pos = np.array([1, 4, 2], dtype='float32')
    pos2 = np.array([9, 8, 7], dtype='float32')
    vel = np.array([0, 1, 0], dtype='float32')
    vel2 = np.array([-3.2, 0.1, -0.1], dtype='float32')
    position = world.component_from_example("Position", pos)
    velocity = world.component_from_example("Velocity", vel)

    e.set(position, pos)
    e.set(velocity, vel)
    e2.set(position, pos2)
    e2.set(velocity, vel2)

    filter = world.filter_builder(position, velocity).build()

    exp_pos = np.stack((pos, pos2))
    exp_vel = np.stack((vel, vel2))

    for val in filter:
        pos_data = val["Position"]
        vel_data = val["Velocity"]

        np.testing.assert_array_equal(pos_data, exp_pos)
        np.testing.assert_array_equal(vel_data, exp_vel)

        pos_data += vel_data

    for val in filter:
        pos_data = val["Position"]
        vel_data = val["Velocity"]

        np.testing.assert_array_equal(pos_data, exp_pos + exp_vel)
        np.testing.assert_array_equal(vel_data, exp_vel)
