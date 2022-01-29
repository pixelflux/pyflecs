"""
Provides access to the flecs entity.
"""
import numpy as np


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
        self._ptr.destruct()

    @property
    def ptr(self):
        return self._ptr

    @property
    def is_alive(self) -> bool:
        return self._ptr.is_alive()

    @property
    def name(self) -> str:
        return self._ptr.name()

    def add(self, component):
        self._ptr.add(component.ptr)

    def set(self, component, value: np.ndarray):
        self._ptr.set(component.ptr, value.view('uint8'))

    def get(self, component) -> np.ndarray:
        return component.create_view(self._ptr.get(component.ptr))[0]

    def remove(self, component):
        self._ptr.remove(component.ptr)

    def __repr__(self) -> str:
        return f"Entity({self._ptr.raw()})"

    def __str__(self) -> str:
        return str(self._ptr.raw())

    def __int__(self) -> int:
        return self._ptr.raw()
