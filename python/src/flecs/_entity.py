"""
Provides access to the flecs entity.
"""
from typing import TYPE_CHECKING, Optional, List
import numpy as np

if TYPE_CHECKING:
    from ._component import Component


class Type:
    """
    Provides a wrapper around the ecs_type_t. This is really an array of
    components, and typically only accessed for debugging purposes.
    """
    def __init__(self, ptr):
        self._ptr = ptr

    def __repr__(self):
        return self._ptr.string()

    def __str__(self):
        return self._ptr.string()

    def __len__(self):
        return self._ptr.length()


class Entity:
    """
    Provides a wrapper around the Flecs entity object.
    """
    def __init__(self, ptr):
        """
        Creates the entity. All entities must be created through the world.

        Args:
            ptr:
        """
        self._ptr = ptr

    def destruct(self):
        # TODO: Should this check that it's not a component?
        self._ptr.destruct()

    @property
    def ptr(self):
        return self._ptr

    @property
    def is_alive(self) -> bool:
        return self._ptr.is_alive()

    @property
    def is_component(self) -> bool:
        return False

    @property
    def is_valid(self) -> bool:
        return self._ptr.is_valid()

    @property
    def type(self) -> Type:
        return Type(self._ptr.type())

    @property
    def name(self) -> str:
        return self._ptr.name()

    def add(self, component: 'Entity'):
        self._ptr.add(component.ptr)
        return self

    def set(self, component: 'Component', value: np.ndarray):
        # Validate the value matches the component dtype
        if value.dtype != component.dtype:
            raise RuntimeError(f"Attempting to set component {component.name} "
                               f"of dtype {component.dtype} to value with "
                               f"dtype {value.dtype}")
        self._ptr.set(component.ptr, value.view('uint8'))
        return self

    def get(self, component: 'Component') -> np.ndarray:
        return component.create_view(self._ptr.get(component.ptr))[0]

    def remove(self, component: 'Entity'):
        self._ptr.remove(component.ptr)
        return self

    def has(self, component: 'Entity') -> bool:
        return self._ptr.has(component.ptr)

    def add_pair(self, component: 'Entity', other: 'Entity'):
        self._ptr.add_pair(component.ptr, other.ptr)
        return self

    def remove_pair(self, component: 'Entity', other: 'Entity'):
        self._ptr.remove_pair(component.ptr, other.ptr)
        return self

    def set_pair(self, component: 'Component', other: 'Entity',
                 value: np.ndarray):
        if value.dtype != component.dtype:
            raise RuntimeError(f"Attempting to set component {component.name} "
                               f"of dtype {component.dtype} to value with "
                               f"dtype {value.dtype}")
        self._ptr.set_pair(component.ptr, other.ptr, value.view('uint8'))
        return self

    def has_pair(self, component: 'Entity', other: 'Entity'):
        return self._ptr.has_pair(component.ptr, other.ptr)

    @property
    def path(self) -> str:
        return self._ptr.path()

    def add_child(self, e: 'Entity'):
        return self._ptr.add_child(e.ptr)

    def lookup(self, name: str) -> Optional['Entity']:
        e = self._ptr.lookup(name)
        return Entity(e) if e.raw() else None

    def is_a(self, e: 'Entity'):
        self._ptr.is_a(e.ptr)

    def __repr__(self) -> str:
        return f"Entity({self._ptr.raw()})"

    def __str__(self) -> str:
        return str(self._ptr.raw())

    def __int__(self) -> int:
        return self._ptr.raw()

    def __eq__(self, other):
        return int(self) == int(other)


class Pair:
    """
    Wraps a pair
    """
    def __init__(self, ptr, relation: Entity, obj: Entity):
        self._ptr = ptr
        self._relation = relation
        self._object = obj

    @property
    def ptr(self):
        return self._ptr

    @property
    def relation(self) -> Entity:
        return self._relation

    @property
    def object(self) -> Entity:
        return self._object


class BulkEntityBuilder:
    """
    Provides a mechanism for creating entities in bulk.
    """
    def __init__(self, ptr):
        self._ptr = ptr

    @property
    def count(self) -> int:
        return self._ptr.count()

    def add(self, e: Entity, data: np.ndarray):
        self._ptr.add(e.ptr, data)

    def build(self) -> List[Entity]:
        results = self._ptr.build()
        return [Entity(val) for val in results]
