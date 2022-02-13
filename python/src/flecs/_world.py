"""
Provides access to the flecs world. This should approximately match the
flecs::world C++ API.
"""
from typing import Optional, Union

import numpy as np
import numpy.typing as npt

import flecs._flecs as _flecs
from ._entity import Entity
from ._component import Component
from ._types import ShapeLike
from ._filter import FilterBuilder, FilterIter, Term, ComponentEntry
from ._query import QueryBuilder


class World:
    """
    Wraps the Flecs World concept using an API similar to the C++ flecs::world
    API.
    """
    def __init__(self):
        self._ptr = _flecs.world()

        # Also store a dictionary of all components.
        self._components = {}

    @property
    def ptr(self):
        return self._ptr

    @property
    def prefab_entity(self) -> Entity:
        """
        Returns the EcsPrefab entity.
        """
        return Entity(self._ptr.EcsPrefab())

    @property
    def childof_entity(self) -> Entity:
        """
        Returns the EcsChildOf entity.
        """
        return Entity(self._ptr.EcsChildOf())

    @property
    def isa_entity(self) -> Entity:
        """
        Returns the EcsChildOf entity.
        """
        return Entity(self._ptr.EcsIsA())

    def prefab(self) -> Entity:
        """
        Returns the Prefab entity. This can be used to create, add, or remove
        from an entity that should be marked as prefab.
        Returns:
            The EcsPrefab entity.
        """
        return Entity(self._ptr.entity(self.prefab_entity.ptr))

    def entity(self, arg: Optional[Union[str, Entity]] = None) -> Entity:
        """
        Creates an entity with the given name.

        Args:
            arg: Either a string name for the entity, or a component to use
                when creating the entity.

        Returns:
            The entity object.
        """
        if arg is not None:
            if isinstance(arg, Entity):
                arg = arg.ptr
            e = self._ptr.entity(arg)
        else:
            e = self._ptr.entity()
        return Entity(e)

    def lookup(self, name: str) -> Optional[Entity]:
        if name in self._components:
            return self._components[name]
        ptr = self._ptr.lookup(name)
        return None if ptr.raw() == 0 else Entity(ptr)

    def lookup_path(self, name: str) -> Optional[Entity]:
        ptr = self._ptr.lookup_path(name)
        return None if ptr.raw() == 0 else Entity(ptr)

    def lookup_by_id(self, eid: int) -> Optional[Entity]:
        e = self._ptr.lookup_by_id(eid)
        name = e.name()
        if name in self._components:
            return self._components[name]
        else:
            return Entity(e)

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
        if name in self._components:
            return self._components[name]
        dtype = np.dtype(dtype)
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
        return FilterBuilder(self, *args, **kwargs)

    def query_builder(self, *args, **kwargs) -> QueryBuilder:
        """
        Creates a query builder, which allows the user to setup a query.
        """
        return QueryBuilder(self, *args, **kwargs)

    def set(self, component: Union[str, Component], data: np.ndarray):
        """
        Sets the singleton value in the world.

        Args:
            component: The component/component name to set.
            data: The data to set.
        """
        if isinstance(component, str):
            name = component
            component = self._components.get(name, None)
            if component is None:
                component = self.component_from_example(name, data)
        self._ptr.set(component.ptr, data.view('uint8'))

    def get(self, component: Union[str, Component]) -> np.ndarray:
        """
        Gets the singleton value.

        Args:
            component: The component to retrieve.

        Returns:
            The data associated with the singleton.
        """
        if isinstance(component, str):
            name = component
            component = self._components.get(name, None)
            if component is None:
                raise RuntimeError(f"Attempting to get component {component} "
                                   f"singleton which does not exist.")
        return component.create_view(self._ptr.get(component.ptr))[0]

    def each(self, term: Union[str, Component, Term]) -> FilterIter:
        """
        Iterates through a single component. This creates a term_iter, but
        uses the FilterIter.

        Args:
            term: The component or Term.

        Returns:
            A FilterIter object.
        """
        if isinstance(term, str):
            name = term
            term = self._components.get(name, None)
            if term is None:
                raise RuntimeError(f"Attempting to iterate over {name} but "
                                   f"component does not exist.")
        if isinstance(term, Component):
            term = Term(term)

        term_iter = self._ptr.create_term_iter(term.ptr)
        component = self.lookup_by_id(term.id)
        # NOTE: term_iter seems to have two values: the component as well as
        # the
        return FilterIter(term_iter, self, [ComponentEntry(component, 1)])
