"""
This is a script to test the timing of operations.
"""
import time

import numpy as np
import flecs


# Set the number of entitites
num_entities = 100000

world = flecs.World()

# Define three components
position = world.component("Position", 'float32', 3)
velocity = world.component("Velocity", 'float32', 3)
acceleration = world.component("Acceleration", 'float32', 3)

# Also add 3 tags
tags = []
tags.append(world.tag("Good"))
tags.append(world.tag("Bad"))
tags.append(world.tag("Ugly"))

# Create the random positions
pos = np.random.randn(num_entities, 3).astype('float32')
vel = np.random.randn(num_entities, 3).astype('float32')
acc = np.random.randn(num_entities, 3).astype('float32')

# Setup which components it should have with a random number
component_type = np.random.rand(num_entities)

# Setup which tag it should have
tag_type = np.random.rand(num_entities)

# Do a basic computation to time it (to give a Python speed baseline)
# This could easily be vectorized, but is a trivial action so this
# really shows Python's overhead.
start_time = time.time()
for idx in range(num_entities):
    ctype = int(component_type[idx] > 0.33) + int(component_type[idx] > 0.66)
    component_type[idx] = ctype
    ttype = int(tag_type[idx] > 0.33) + int(tag_type[idx] > 0.66)
    tag_type[idx] = ttype
print(f"Took {time.time() - start_time} for simple setup")

# Now create the entities and assign components
start_time = time.time()
for idx in range(num_entities):
    e = world.entity()
    e.set(position, pos[idx])
    if component_type[idx] > 0:
        e.set(velocity, vel[idx])
    if component_type[idx] > 1:
        e.set(acceleration, acc[idx])
    e.add(tags[0])
    if tag_type[idx] > 0:
        e.add(tags[1])
    if tag_type[idx] > 1:
        e.add(tags[2])
print(f"Took {time.time() - start_time} for component creation")

# Now do a loop where we handle each component type
filter_pos = world.query_builder(position).build()
filter_vel = world.query_builder(position, velocity).build()
filter_acc = world.query_builder(position, velocity, acceleration).build()

# Finally get a filter or concatenating all of the positions for "Good"
filter_good = world.query_builder(position, tags[0]).build()

start_time = time.time()
for val in filter_pos:
    pos = val["Position"]
for val in filter_vel:
    pos = val["Position"]
    pos += val["Velocity"]

for val in filter_acc:
    pos = val["Position"]
    vel = val["Velocity"]
    pos += vel + 0.5 * val["Acceleration"]**2
    vel += val["Acceleration"]

results = []
for val in filter_good:
    results.append(val["Position"])
final_result = np.vstack(results)
print(f"Took {time.time() - start_time} sec to run filters. "
      f"Got {len(final_result)} good results")