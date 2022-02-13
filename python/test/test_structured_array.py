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


def test_structured_query():
    """
    Tests that a structured array will work in a query.
    """
    num_entities = 1000

    world = flecs.World()

    info1_data = np.array([1, 2, 3], dtype=[('a', 'uint32'), ('b', 'float'),
                                            ('c', 'uint8')])
    info2_data = np.array([1, 2, 3, 4, 5],
                          dtype=[('x', 'uint8'), ('y', 'float32'),
                                 ('z', 'uint16'), ('aa', 'float'),
                                 ('bb', 'int8')])

    info3_data = np.array([1, 2], dtype=[('foo', 'uint8'), ('bar', 'uint16')])


    # Define three components
    info1 = world.component_from_example("Info1", info1_data)
    info2 = world.component_from_example("Info2", info2_data)
    info3 = world.component_from_example("Info3", info3_data)

    # Note tags
    info12_tag = world.tag("Info12")
    info13_tag = world.tag("Info13")
    info23_tag = world.tag("Info23")

    # Also add 3 tags
    tags = []
    tags.append(world.tag("Good"))
    tags.append(world.tag("Bad"))
    tags.append(world.tag("Ugly"))

    # Setup which components it should have with a random number
    rng = np.random.default_rng(1)
    component_type = rng.random(num_entities)

    # Setup which tag it should have
    tag_type = rng.random(num_entities)

    for idx in range(num_entities):
        ctype = int(component_type[idx] > 0.33) + int(
            component_type[idx] > 0.66)
        component_type[idx] = ctype
        ttype = int(tag_type[idx] > 0.33) + int(tag_type[idx] > 0.66)
        tag_type[idx] = ttype

    total_good = 0
    for idx in range(num_entities):
        e = world.entity()
        if component_type[idx] == 0:
            e.set(info1, info1_data)
            e.set(info2, info2_data)
            e.add(info12_tag)
        elif component_type[idx] == 1:
            e.set(info1, info1_data)
            e.set(info3, info3_data)
            e.add(info13_tag)
        else:
            e.set(info2, info2_data)
            e.set(info3, info3_data)
            e.add(info23_tag)

        if tag_type[idx] == 0:
            e.add(tags[0])
            total_good += 1
        elif tag_type[idx] == 1:
            e.add(tags[1])
        else:
            e.add(tags[2])

    filter_12 = world.filter_builder(info1, info2, info12_tag).build()
    filter_13 = world.filter_builder(info1, info3, info13_tag).build()
    filter_23 = world.filter_builder(info2, info3, info23_tag).build()
    filter_good = world.filter_builder(
        expr='?Info1, ?Info2, ?Info3, Good').build()

    for val in filter_12:
        np.testing.assert_array_equal(info1_data, val["Info1"][0])
        np.testing.assert_array_equal(info2_data, val["Info2"][0])
        np.testing.assert_array_equal(info1_data, val["Info1"][-1])
        np.testing.assert_array_equal(info2_data, val["Info2"][-1])

    for val in filter_13:
        np.testing.assert_array_equal(info1_data, val["Info1"][0])
        np.testing.assert_array_equal(info3_data, val["Info3"][0])
        np.testing.assert_array_equal(info1_data, val["Info1"][-1])
        np.testing.assert_array_equal(info3_data, val["Info3"][-1])

    for val in filter_23:
        np.testing.assert_array_equal(info2_data, val["Info2"][0])
        np.testing.assert_array_equal(info3_data, val["Info3"][0])
        np.testing.assert_array_equal(info2_data, val["Info2"][-1])
        np.testing.assert_array_equal(info3_data, val["Info3"][-1])

    # Match total_good
    match_good = 0
    for val in filter_good:
        match_good += len(val)

    assert total_good == match_good
