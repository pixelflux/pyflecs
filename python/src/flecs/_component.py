"""
Provides access to the flecs component.
"""
import numpy as np
from numpy.typing import DTypeLike

from ._types import ShapeLike


class Component:
    """
    Wraps a flecs component
    """
    def __init__(self, ptr, dtype: DTypeLike, shape: ShapeLike):
        self._ptr = ptr
        self._dtype = dtype

        if isinstance(shape, int):
            shape = [shape]
        self._shape = shape

        # Store the total bytes
        self._nbytes = np.prod(shape) * dtype.itemsize

    @property
    def ptr(self):
        return self._ptr

    def create_view(self, buffer: np.ndarray) -> np.ndarray:
        """
        This creates a view into the buffer that matches the component dtype.

        Args:
            buffer: This should be a raw array of data for this component type.

        Returns:
            A view of the numpy array that matches the original dtype
            and shape.
        """
        num_elem = buffer.nbytes // self._nbytes
        new_shape = (num_elem, *self._shape)
        return buffer.view(self._dtype).reshape(new_shape)
