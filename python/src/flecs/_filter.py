"""
Wraps various aspects of the flecs filters.
"""
from typing import TYPE_CHECKING, List, Optional, Union
from collections import namedtuple

import flecs._flecs as _flecs
from ._entity import Entity

if TYPE_CHECKING:
    from ._world import World


_ComponentEntry = namedtuple("_ComponentEntry", ['component', 'index'])
"""Defines an object for storing component information."""


class Term:
    """
    Wraps the Flecs term object.
    """
    def __init__(self, id: Optional[Entity] = None):
        self._ptr = _flecs.ecs_term_t()
        self._id = id
        if id is not None:
            self._ptr.id = id.ptr.raw()

    @property
    def ptr(self):
        return self._ptr

    @property
    def id(self) -> Entity:
        return self._id

    @id.setter
    def id(self, val: Entity):
        self._id = val
        self._ptr.id = val.ptr.raw()


class FilterIter:
    """
    Provides a wrapper around iteration of a filter.
    """
    def __init__(self, ptr, components: List[_ComponentEntry]):
        self._ptr = ptr
        self._components = components

        # Create a dictionary of the components as well
        self._component_dict = {val.component.name: val for val in components}

    def __next__(self):
        if self._ptr.next():
            return self
        else:
            raise StopIteration

    def __getitem__(self, item):
        if isinstance(item, int):
            info = self._components[item]
        else:
            info = self._component_dict[item]
        return info.component.create_view(
            self._ptr.term(info.component.ptr, info.index))


class Filter:
    """
    Provides access to a filter that was created.
    """
    def __init__(self, ptr, world: 'World'):
        self._ptr = ptr

        # Lookup components
        self._components = []
        for idx in range(ptr.term_count()):
            term = ptr.terms(idx)
            component = world.lookup_by_id(term.id)
            self._components.append(_ComponentEntry(
                component=component, index=idx+1))

    def __iter__(self) -> FilterIter:
        return FilterIter(self._ptr.iter(), self._components)


class FilterBuilder:
    """
    Class for building up a filter.
    """
    def __init__(self, world: 'World', *args, name: str = ''):
        self._world = world
        self._terms = []
        self._components = []
        # For now, do not support expr. Otherwise we would need to parse it to
        # identify the components.
        self._expr = ''
        self._name = name

        for arg in args:
            self.term(arg)

    def term(self, val: Union[Term, 'Entity']) -> 'FilterBuilder':
        """
        Appends the term to the list of terms to add to the filter.

        Args:
            val: The entity to add to the filter.

        Returns:
            This object, allowing for chains.
        """
        # Append the raw ID
        if not isinstance(val, Term):
            val = Term(val)

        self._terms.append(val.ptr)
        return self

    @property
    def expr(self) -> str:
        return self._expr

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: str):
        """
        Sets the name of the filter.

        Args:
            val: The name to give the filter. Used for debugging purposes.
        """
        self._name = val

    def build(self) -> Filter:
        """
        Builds the filter.

        Args:
            build_query: If true, builds a query instead.

        Returns:
            The filter object.
        """
        # Build the raw filter
        ptr = self._world.ptr.create_filter(self._name, self._expr,
                                            self._terms)
        return Filter(ptr, self._world)
