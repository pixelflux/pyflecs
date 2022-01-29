"""
This script follows the flecs quickstart
"""
import pyflecs as flecs

world = flecs.world()

# Create an entity
e = world.entity()
print(e.is_alive())
e.destruct()
print(e.is_alive())


e = world.entity("Bob")
print(f"Entity name: {e.name()}")
