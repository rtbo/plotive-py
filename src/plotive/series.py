"""Data series objects that can be rendered in a plot."""

from abc import ABC
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from .color import Color

type DataCol = str | list[float] | list[str] | np.ndarray
"""Data column reference, Python sequence, or NumPy array."""

type AxisRef = str | int
"""Axis reference by string identifier or numeric index."""

class Series(ABC):
    """Base class for plot series objects."""

    def __init__(
        self,
        *,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        """Initialize common series metadata.

        Parameters
        ----------
        name : str | None, default=None
            Legend/display name of the series.
        x_axis : AxisRef | None, default=None
            Target x-axis reference.
        y_axis : AxisRef | None, default=None
            Target y-axis reference.
        """
        self.name = name
        self.x_axis = x_axis
        self.y_axis = y_axis

    def _get_type(self) -> str:
        """Return the concrete series type name."""
        return self.__class__.__name__


class Line(Series):
    """Line series defined by x/y coordinates."""

    def __init__(
        self,
        x: DataCol,
        y: DataCol,
        *,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
        linewidth: None | float = None,
        linestyle: None | str | list[float] = None,
        color: None | Color = None,
        interpolation: None | str = None,
    ):
        """Initialize a line series.

        Parameters
        ----------
        x : DataCol
            X values or x data source reference.
        y : DataCol
            Y values or y data source reference.
        name : str | None, default=None
            Legend/display name of the series.
        x_axis : AxisRef | None, default=None
            Target x-axis reference.
        y_axis : AxisRef | None, default=None
            Target y-axis reference.
        linewidth : float | None, default=None
            Override line width.
        linestyle : str | list[float] | None, default=None
            Line style or dash pattern.
        color : Color | None, default=None
            Line color.
        interpolation : str | None, default=None
            Interpolation mode for rendering.
        """
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = x
        self.y = y
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = color
        self.interpolation = interpolation
