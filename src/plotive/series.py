"""Data series objects that can be rendered in a plot."""

from abc import ABC
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from datetime import datetime
    from . import axis

from .cmap import BuiltinCmap, ColorMap
from .style import Color, Fill, Marker, Stroke, _parse_mpl_style

type DataCol = str | list[float] | list[int] | list[str] | list[datetime] | np.ndarray
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
        stroke: Stroke | Color = "auto",
        interp: None | str = None,
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
        interp : str | None, default=None
            interp mode for rendering.
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
        self.x = x
        self.y = y
        self.stroke = Stroke._normalize(stroke, default_width=1.5)
        self.interp = interp
        self.marker = marker
        self.style = style
        if style is not None:
            marker_shape, line_pattern, line_color = _parse_mpl_style(style)
            if marker_shape is not None:
                if self.marker is None:
                    self.marker = Marker(shape=marker_shape)
                else:
                    self.marker.shape = marker_shape
            if line_pattern is not None:
                self.stroke.pattern = line_pattern
            if line_color is not None:
                self.stroke.color = line_color
        if width is not None:
            self.stroke.width = width


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
        cmap: None | ColorMap | list[Color] | BuiltinCmap = "viridis",
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
        cmap : ColorMap | list[Color] | str | None, default="viridis"
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
        self.x = x
        self.y = y
        self.sizes = sizes
        self.marker = marker if marker is not None else Marker()
        self.colors = colors
        assert not (
            self.colors is not None and cmap is None
        ), "cmap must be specified if colors are provided"
        self.cmap = ColorMap._normalize(cmap) if cmap is not None else None


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
        self.x = x
        self.y1 = y1
        self.y2 = y2
        self.fill = Fill._normalize(fill)
        self.y1_stroke = (
            Stroke._normalize(y1_stroke, default_width=1.5)
            if y1_stroke is not None
            else None
        )
        self.y2_stroke = (
            Stroke._normalize(y2_stroke, default_width=1.5)
            if y2_stroke is not None
            else None
        )
        self.y1_interp = y1_interp or interp
        self.y2_interp = y2_interp or interp


class Histogram(Series):
    def __init__(
        self,
        data: DataCol,
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
        self.data = data
        self.fill = Fill._normalize(fill) if fill is not None else None
        self.stroke = (
            Stroke._normalize(stroke, default_width=1.5) if stroke is not None else None
        )
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
        bars_offset=0.3,
        bars_width=0.4,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = x
        self.y = y
        self.fill = Fill._normalize(fill) if fill is not None else None
        self.stroke = (
            Stroke._normalize(stroke, default_width=1.5) if stroke is not None else None
        )
        self.bars_offset = bars_offset
        self.bars_width = bars_width
