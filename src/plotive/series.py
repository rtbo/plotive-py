"""Data series objects that can be rendered in a plot."""

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, cast
import numpy as np

if TYPE_CHECKING:
    from . import axis

from .cmap import ColorMap
from . import mapping
from .style import (
    Color,
    Fill,
    Marker,
    Pattern,
    SeriesColor,
    SeriesStroke,
    Stroke,
    _parse_mpl_style,
)

type DataCol = str | list[float] | list[int] | list[str] | list[datetime] | np.ndarray
"""Data column reference, Python sequence, or NumPy array."""


def _normalize_data_col(
    data: DataCol | None,
) -> list[float] | list[int] | list[str] | str | None:
    """Normalize a data column to a list."""
    if data is None:
        return None
    if isinstance(data, str):
        return data
    if isinstance(data, np.ndarray):
        return data.tolist()
    if isinstance(data, list):
        if data and isinstance(data[0], datetime):
            return list(map(lambda dt: dt.isoformat(), data))  # type: ignore
        return cast(list[float] | list[int] | list[str], data)
    else:
        raise TypeError(f"Unsupported data column type: {type(data)}")


type AxisRef = str | int
"""Axis reference by string identifier or numeric index."""


class Series(ABC, mapping.PvMapping):
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
        self.type = self.__class__.__name__.lower().replace("histogram", "hist")
        self.name = name
        self.x_axis = x_axis
        self.y_axis = y_axis


class Line(Series):
    """Line series defined by x/y coordinates."""

    def __init__(
        self,
        x: DataCol,
        y: DataCol,
        *,
        stroke: SeriesStroke | SeriesColor = "auto",
        interpolation: None | str = None,
        marker: Marker | None = None,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
        style: None | str = None,
        width: None | float = None,
    ):
        """Initialize a line series.

        Parameters
        ----------
        x : DataCol
            X values or x data source reference.
        y : DataCol
            Y values or y data source reference.
        line : Stroke | Color, default="auto"
            Line stroke style or color.
        interpolation : str | None, default=None
            Interpolation mode for rendering.
        marker : Marker | None, default=None
            Marker style. If None, no marker will be rendered.
        name : str | None, default=None
            Legend/display name of the series.
        x_axis : AxisRef | None, default=None
            Target x-axis reference.
        y_axis : AxisRef | None, default=None
            Target y-axis reference.
        style: None | str, default=None
            Optional style shorthand string for quick styling.
            It is compatible with matplotlib's style syntax for line properties.
        width: None | float, default=None
            Optional shorthand to specify the line width in points.
        """
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = _normalize_data_col(x)
        self.y = _normalize_data_col(y)
        self.stroke = stroke
        self.interpolation = interpolation
        self.marker = marker

        if style is not None:
            shape, pattern, color = _parse_mpl_style(style)

            if shape is not None:
                if self.marker is None:
                    self.marker = Marker(shape=shape)
                else:
                    self.marker.shape = shape

            if pattern is not None:
                if isinstance(self.stroke, str):
                    self.stroke = Stroke(color=self.stroke, pattern=pattern)
                elif isinstance(self.stroke, Stroke):
                    self.stroke.pattern = pattern

            if color is not None:
                if isinstance(self.stroke, str):
                    self.stroke = Stroke(color=color)
                elif isinstance(self.stroke, Stroke):
                    self.stroke = Stroke(
                        color=color,
                        pattern=cast(Pattern | None, self.stroke.pattern),
                    )

        if width is not None:
            if isinstance(self.stroke, str):
                self.stroke = Stroke(color=self.stroke, width=width)
            elif isinstance(self.stroke, Stroke):
                self.stroke.width = width
            elif self.stroke is None:
                self.stroke = Stroke(color="auto", width=width)


class Scatter(Series):
    """Scatter series defined by x/y coordinates."""

    def __init__(
        self,
        x: DataCol,
        y: DataCol,
        *,
        marker: Marker | None = None,
        sizes: None | DataCol = None,
        colors: None | DataCol = None,
        color_cats_to_legend: bool = False,
        cmap: None | ColorMap = None,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        """Initialize a scatter series.

        Parameters
        ----------
        x : DataCol
            X values or x data source reference.
        y : DataCol
            Y values or y data source reference.
        sizes : DataCol | None, default=None
            Optional marker sizes specified as a data column or sequence.
            If specified, the marker size will be multiplied by the size value for each point.
            Note that the marker size is an area measurement, so the size value will be interpreted as a scaling factor for the marker area.
        colors : DataCol | None, default=None
            Optional marker colors specified as a data column or sequence.
            If specified, the marker color will be determined by mapping the color value for each point through the colormap specified by `cmap`.
        color_cats_to_legend : bool, default=False
            If True, the color categories will be added to the legend as categorical entries.
        cmap : ColorMap | list[Color] | str | None, default=None
            Colormap specification for mapping color values to marker colors.
             - If a ColorMap object is provided, it will be used directly.
             - If a list of Colors is provided, it will be used to create a ColorMap with default settings.
             - If a string is provided, it will be interpreted as a named colormap and used to create a ColorMap with default settings.
             - If None, a default colormap will be used if `colors` is specified, otherwise no colormap will be applied.
            Ignored if `colors` is not specified.
        marker : Marker, default=None
            Marker style. If None, the marker will be automatically assigned based on the series palette.
        name : str | None, default=None
            Legend/display name of the series.
        x_axis : AxisRef | None, default=None
            Target x-axis reference.
        y_axis : AxisRef | None, default=None
            Target y-axis reference.
        """
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = _normalize_data_col(x)
        self.y = _normalize_data_col(y)
        self.sizes = _normalize_data_col(sizes)
        self.marker = marker if marker is not None else Marker()
        self.colors = _normalize_data_col(colors)
        self.color_cats_to_legend = color_cats_to_legend
        self.cmap = cmap


class Area(Series):
    """Area series defined by x/y1/y2 coordinates.

    Y1 and Y2 define the upper and lower bounds of the area, or vice versa.
    Y2 can be a constant value and defaults to 0.
    """

    def __init__(
        self,
        x: DataCol,
        y1: DataCol,
        y2: DataCol | float = 0,
        *,
        fill: Fill | Color = "auto",
        y1_stroke: Stroke | Color | None = None,
        y2_stroke: Stroke | Color | None = None,
        y1_interp: None | str = None,
        y2_interp: None | str = None,
        interp: None | str = None,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        """Initialize an area series.

        Parameters
        ----------
        x : DataCol
            X values or x data source reference.
        y1 : DataCol
            Y1 values or y1 data source reference.
        y2 : DataCol | float, default=0
            Y2 values or y2 data source reference. Can be a constant value.
        fill : Fill | Color, default="auto"
            Area fill style or color.
        y1_stroke : Stroke | Color | None, default=None
            Area stroke stroke style or color for Y1.
        y2_stroke : Stroke | Color | None, default=None
            Area stroke stroke style or color for Y2.
        y1_interp : str | None, default=None
            interp mode for y1 rendering. If None, defaults to the value of `interp`.
        y2_interp : str | None, default=None
            interp mode for y2 rendering. If None, defaults to the value of `interp`.
            Ignored if y2 is a constant value.
        interp : str | None, default=None
            interp mode for rendering. If specified, applies to both y1 and y2.
        name : str | None, default=None
            Legend/display name of the series.
        x_axis : AxisRef | None, default=None
            Target x-axis reference.
        y_axis : AxisRef | None, default=None
            Target y-axis reference.
        """
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = _normalize_data_col(x)
        self.y1 = _normalize_data_col(y1)
        self.y2 = _normalize_data_col(y2) if not isinstance(y2, (int, float)) else y2
        self.fill = fill
        self.y1_stroke = y1_stroke
        self.y2_stroke = y2_stroke
        self.y1_interp = y1_interp or interp
        self.y2_interp = y2_interp or interp


class Histogram(Series):
    def __init__(
        self,
        x: DataCol,
        *,
        fill: None | Fill | Color = "auto",
        stroke: None | Stroke | Color = None,
        bins: int = 10,
        density: bool = False,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = _normalize_data_col(x)
        self.fill = fill
        self.stroke = stroke
        self.bins = bins
        self.density = density


class Bars(Series):
    def __init__(
        self,
        x: DataCol,
        y: DataCol,
        *,
        fill: None | Fill | Color = "auto",
        stroke: None | Stroke | Color = None,
        position: None | tuple[float, float] = None,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = _normalize_data_col(x)
        self.y = _normalize_data_col(y)
        self.fill = fill
        self.stroke = stroke
        self.position = position
