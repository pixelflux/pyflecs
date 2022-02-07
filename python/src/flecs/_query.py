"""
Wraps the query. The query is different from a filter, but includes a filter.
"""
from typing import TYPE_CHECKING

from ._filter import FilterIter, FilterBuilder, _ComponentEntry

if TYPE_CHECKING:
    from ._world import World


class Query:
    """
    Provides access to a query that was created.

    TODO: This is identical to Filter currently.
    """
    def __init__(self, ptr, world: 'World'):
        self._ptr = ptr

        # Lookup components
        self._components = []
        for idx in range(ptr.term_count()):
            term = ptr.terms(idx)
            component = world.lookup_by_id(term.id)
            self._components.append(_ComponentEntry(
                component=component, index=idx + 1))

    def __iter__(self):
        return FilterIter(self._ptr.iter(), self._components)


class QueryBuilder(FilterBuilder):
    """
    Provides a builder for a query. The same as a filter builder, but creates
    a query in the end instead.
    """
    def build(self) -> Query:
        ptr = self._world.ptr.create_query(self._name, self._expr, self._terms)
        return Query(ptr, self._world)
