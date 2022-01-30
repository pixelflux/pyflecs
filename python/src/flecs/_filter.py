"""
Wraps various aspects of the flecs filters.
"""
from typing import TYPE_CHECKING, List
from collections import namedtuple

import numpy as np

if TYPE_CHECKING:
    from ._world import World
    from ._entity import Entity


_ComponentEntry = namedtuple("_ComponentEntry", ['component', 'index'])
"""Defines an object for storing component information."""


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
    def __init__(self, ptr, components: List[_ComponentEntry]):
        self._ptr = ptr
        self._components = components

    def __iter__(self) -> FilterIter:
        return FilterIter(self._ptr.iter(), self._components)


class FilterBuilder:
    """
    Class for building up a filter.
    """
    def __init__(self, world, *args, expr: str = '', name: str = ''):
        self._world = world
        self._terms = []
        self._components = []
        self._expr = expr
        self._name = name

        for arg in args:
            self.term(arg)

    def term(self, val: 'Entity') -> 'FilterBuilder':
        """
        Appends the term to the list of terms to add to the filter.

        Args:
            val: The entity to add to the filter.

        Returns:
            This object, allowing for chains.
        """
        # Append the raw ID
        self._terms.append(val.ptr)
        if val.is_component:
            self._components.append(_ComponentEntry(val, len(self._terms)))
        return self

    @property
    def expr(self) -> str:
        return self._expr

    @expr.setter
    def expr(self, val: str):
        """
        Allows setting the expression for the filter.

        Args:
            val: The filter expression.
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

        Returns:
            The filter object.
        """
        # Build the raw filter
        ptr = self._world.create_filter(self._name, self._expr, self._terms)
        return Filter(ptr, self._components)
