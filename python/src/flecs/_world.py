"""
Provides access to the flecs world. This should approximately match the
flecs::world C++ API.
"""
from typing import Optional

import numpy as np
import numpy.typing as npt

import flecs._flecs as _flecs
from ._entity import Entity
from ._component import Component
from ._types import ShapeLike


class World:
    """
    Wraps the Flecs World concept using an API similar to the C++ flecs::world
    API.
    """
    def __init__(self):
        self._ptr = _flecs.world()

    def entity(self, name: Optional[str] = None) -> Entity:
        """
        Creates an entity with the given name.

        Args:
            name: The name of the entity.

        Returns:
            The entity object.
        """
        e = self._ptr.entity() if name is None else self._ptr.entity(name)
        return Entity(e)

    def lookup(self, name: str) -> Entity:
        return Entity(self._ptr.lookup(name))


    def component(self, name: str, dtype: npt.DTypeLike,
                  shape: ShapeLike = 1) -> Component:
        """
        Creates a component with the given name. This requires knowing the
        dtype of the component, as well as the shape. Another way to initialize
        a component from an existing field is using "component_from_example".

        Args:
            name: The name of the component.
            dtype: The data type of the component.
            shape: The shape of the component.

        Returns:
            The component.
        """
        nbytes = np.prod(shape) * dtype.itemsize
        c = self._ptr.component(name, nbytes, dtype.alignment)
        return Component(c, dtype, shape)

    def component_from_example(self, name: str, example: npt.ArrayLike):
        """
        Creates a component with the given name from the example numpy array.

        Args:
            name: The name of the component.
            example: An example of the data type to wrap.

        Returns:
            The component
        """
        c = self._ptr.component(name, example.nbytes, example.dtype.alignment)
        return Component(c, example.dtype, example.shape)