from abc import ABC
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from .color import Color

type DataCol = str | list[float] | list[str] | np.ndarray
type AxisRef = str | int

class Series(ABC):
    def __init__(
        self,
        *,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        self.name = name
        self.x_axis = x_axis
        self.y_axis = y_axis

    def _get_type(self) -> str:
        return self.__class__.__name__


class Line(Series):
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
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = x
        self.y = y
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.color = color
        self.interpolation = interpolation
