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
from ._filter import FilterBuilder


class World:
    """
    Wraps the Flecs World concept using an API similar to the C++ flecs::world
    API.
    """
    def __init__(self):
        self._ptr = _flecs.world()

        # Also store a dictionary of all components.
        self._components = {}

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

    def lookup(self, name: str) -> Optional[Entity]:
        if name in self._components:
            return self._components[name]
        ptr = self._ptr.lookup(name)
        return None if ptr.raw() == 0 else Entity(ptr)

    def lookup_path(self, name: str) -> Optional[Entity]:
        ptr = self._ptr.lookup_path(name)
        return None if ptr.raw() == 0 else Entity(ptr)

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
        dtype = np.dtype(dtype)
        if name in self._components:
            return self._components[name]
        nbytes = np.prod(shape) * dtype.itemsize
        raw_component = self._ptr.component(name, nbytes, dtype.alignment)
        c = Component(raw_component, dtype, shape)
        self._components[name] = c
        return c

    def component_from_example(self, name: str, example: npt.ArrayLike):
        """
        Creates a component with the given name from the example numpy array.

        Args:
            name: The name of the component.
            example: An example of the data type to wrap.

        Returns:
            The component
        """
        if name in self._components:
            return self._components[name]
        raw_component = self._ptr.component(name, example.nbytes,
                                            example.dtype.alignment)
        c = Component(raw_component, example.dtype, example.shape)
        self._components[name] = c
        return c

    def tag(self, name: str) -> Entity:
        """
        Creates an empty component, which is a tag.
        Args:
            name: The name of the tag.

        Returns:
            The component representing the tag.
        """
        c = self._ptr.component(name, 0, 0)
        return Entity(c)

    def filter_builder(self, *args, **kwargs) -> FilterBuilder:
        """
        Creates a filter builder, which allows the user to setup a filter.
        """
        return FilterBuilder(self._ptr, *args, **kwargs)
