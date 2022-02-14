"""
Wraps various aspects of the flecs filters.
"""
from typing import TYPE_CHECKING, List, Optional, Union
from collections import namedtuple

import flecs._flecs as _flecs

from ._component import Component
from ._entity import Entity

if TYPE_CHECKING:
    from ._world import World


ComponentEntry = namedtuple("ComponentEntry", ['component', 'index'])
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


class EntitiesIter:
    """
    Provides a helper wrapper around the entities attached to a FilterIter.
    """
    def __init__(self, ptr, world: 'World'):
        # Uses the same pointer as the FilterIter.
        self._ptr = ptr
        self._world = world
        self._idx = 0

    def __len__(self):
        return self._ptr.count()

    def __getitem__(self, item) -> Union[List[Entity], Entity]:
        if isinstance(item, slice):
            results = []
            start_idx = item.start or 0
            end_idx = item.stop or len(self)
            step = item.step or 1
            for idx in range(start_idx, end_idx, step):
                results.append(self._world.lookup_by_id(
                    self._ptr.get_entity(idx)))
            return results
        else:
            e = self._ptr.get_entity(item)
            return self._world.lookup_by_id(e)

    def __next__(self):
        if self._idx >= len(self):
            raise StopIteration
        self._idx += 1
        return self[self._idx - 1]

    def __iter__(self):
        self._idx = 0
        return self


class FilterIter:
    """
    Provides a wrapper around iteration of a filter.
    """
    def __init__(self, ptr, world: 'World',
                 components: List[ComponentEntry]):
        self._ptr = ptr
        self._world = world

        # Create a dictionary of the components as well
        self._components = components
        self._component_dict = {val.component.name: val for val in components}

    def __contains__(self, item):
        return item in self._component_dict

    def __len__(self) -> int:
        return self._ptr.count()

    def __next__(self):
        if self._ptr.next():
            return self
        else:
            raise StopIteration

    def __iter__(self):
        return self

    def __getitem__(self, item):
        if isinstance(item, int):
            info = self._components[item]
        else:
            info = self._component_dict[item]
        data = self._ptr.data(info.component.ptr, info.index)
        return info.component.create_view(data)

    @property
    def term_count(self) -> int:
        return self._ptr.term_count()

    @property
    def entities(self) -> EntitiesIter:
        """
        Returns the entity for the given index.
        Args:
            idx: The index to retrieve the entity.

        Returns:
            An EntitiesIter object.
        """
        return EntitiesIter(self._ptr, self._world)


class Filter:
    """
    Provides access to a filter that was created.
    """
    def __init__(self, ptr, world: 'World'):
        self._ptr = ptr
        self._world = world

        # Lookup components
        self._components = []
        for idx in range(ptr.term_count()):
            term = ptr.terms(idx)
            component = world.lookup_by_id(term.id)
            self._components.append(ComponentEntry(
                component=component, index=idx+1))

    def __iter__(self) -> FilterIter:
        return FilterIter(self._ptr.iter(), self._world, self._components)


class FilterBuilder:
    """
    Class for building up a filter.
    """
    def __init__(self, world: 'World', *args, name: str = '', expr: str = '',
                 instanced: bool = False):
        self._world = world
        self._terms = []
        self._components = []
        self._expr = expr
        self._name = name
        self._instanced = instanced

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

    @expr.setter
    def expr(self, val: str):
        """
        Sets the expression for the filter.

        Args:
            val: The expression string
        """
        self._expr = val

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
                                            self._instanced, self._terms)
        return Filter(ptr, self._world)
