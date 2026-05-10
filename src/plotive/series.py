"""Data series objects that can be rendered in a plot."""

from abc import ABC
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from datetime import datetime
    from .style import SeriesColor
    from . import axis

from .style import Color, SeriesFill, SeriesMarker, SeriesStroke

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
        line: SeriesStroke | SeriesColor = SeriesStroke(),
        interpolation: None | str = None,
        marker: SeriesMarker | None = None,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        """Initialize a line series.

        Parameters
        ----------
        x : DataCol
            X values or x data source reference.
        y : DataCol
            Y values or y data source reference.
        line : SeriesStroke | SeriesColor | None, default=None
            Line stroke style or color.
        interpolation : str | None, default=None
            Interpolation mode for rendering.
        marker : SeriesMarker | None, default=None
            Marker style. If None, no marker will be rendered.    let ?;
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
        self.line = SeriesStroke._normalize(line)
        self.interpolation = interpolation
        self.marker = marker


class ColorMap:
    def __init__(
        self,
        cmap: str | list[Color],
        method: str | None ="auto",
        scale: None | axis.Scale = None,
    ):
        """Initializes a colormap

        Parameters
        ----------
        cmap : str | list[Color]
            Colormap name or list of colors.
        method : str | None, default="auto"
            Interpolation method for the colormap.
            Ignored if `cmap` isn't a list of colors.
            Accepted values are:
                - "auto":
                        - If the list has fewer than 256 colors, use "linear" interpolation.
                        - If the list has 256 colors or more, use "nearest" interpolation,
                         since the colormap is already at the maximum resolution typically used for rendering.
                - None: using nearest neighbor
                - "nearest: same as None
                - "srgb" (interpolation in sRGB color space)
                - "fast": same as "srgb"
                - "linear" (interpolation in linear RGB color space)
                - "perceptual" (interpolation in OkLab color space)
        scale : Scale | None, default=None
            Optional scale for mapping data values to the colormap. If None, a default linear scale will be used,
            that maps the full data range to the full colormap.
        """
        self.cmap = cmap
        if method is None:
            method = "nearest"
        if method == "fast":
            method = "srgb"
        if method == "auto" and isinstance(cmap, list):
            method = "linear" if len(cmap) < 256 else "nearest"
        self.method = method
        self.scale = scale

    @staticmethod
    def _normalize(input: str | list[Color] | ColorMap) -> "ColorMap":
        if isinstance(input, ColorMap):
            return input
        elif isinstance(input, str) or isinstance(input, list):
            return ColorMap(cmap=input)
        else:
            raise ValueError(f"Invalid colormap specification: {input}")


class Scatter(Series):
    """Scatter series defined by x/y coordinates."""

    def __init__(
        self,
        x: DataCol,
        y: DataCol,
        *,
        marker: SeriesMarker = SeriesMarker(),
        sizes: None | DataCol = None,
        colors: None | DataCol = None,
        cmap: None | ColorMap | list[Color] | str = "viridis",
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
        marker : SeriesMarker, default=SeriesMarker()
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
        self.marker = marker
        self.colors = colors
        assert not (self.colors is not None and cmap is None), "cmap must be specified if colors are provided"
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
        fill: SeriesFill | SeriesColor = SeriesFill(),
        y1_line: SeriesStroke | SeriesColor | None = None,
        y2_line: SeriesStroke | SeriesColor | None = None,
        y1_interpolation: None | str = None,
        y2_interpolation: None | str = None,
        interpolation: None | str = None,
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
        fill : SeriesFill | SeriesColor, default=SeriesFill()
            Area fill style or color.
        y1_line : SeriesStroke | SeriesColor, default=SeriesStroke()
            Area outline stroke style or color for Y1.
        y2_line : SeriesStroke | SeriesColor, default=SeriesStroke()
            Area outline stroke style or color for Y2.
        y1_interpolation : str | None, default=None
            Interpolation mode for y1 rendering. If None, defaults to the value of `interpolation`.
        y2_interpolation : str | None, default=None
            Interpolation mode for y2 rendering. If None, defaults to the value of `interpolation`.
            Ignored if y2 is a constant value.
        interpolation : str | None, default=None
            Interpolation mode for rendering. If specified, applies to both y1 and y2.
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
        self.fill = SeriesFill._normalize(fill)
        self.y1_line = SeriesStroke._normalize(y1_line) if y1_line is not None else None
        self.y2_line = SeriesStroke._normalize(y2_line) if y2_line is not None else None
        self.y1_interpolation = y1_interpolation or interpolation
        self.y2_interpolation = y2_interpolation or interpolation


class Histogram(Series):
    def __init__(
        self,
        data: DataCol,
        *,
        fill: None | SeriesFill | SeriesColor = "auto",
        outline: None | SeriesStroke | SeriesColor = None,
        bins: int = 10,
        density: bool = False,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.data = data
        self.fill = SeriesFill._normalize(fill) if fill is not None else None
        self.outline = SeriesStroke._normalize(outline) if outline is not None else None
        self.bins = bins
        self.density = density


class Bars(Series):
    def __init__(
        self,
        x: DataCol,
        y: DataCol,
        *,
        fill: None | SeriesFill | SeriesColor = "auto",
        outline: None | SeriesStroke | SeriesColor = None,
        bars_offset=0.3,
        bars_width=0.4,
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
    ):
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = x
        self.y = y
        self.fill = SeriesFill._normalize(fill) if fill is not None else None
        self.outline = SeriesStroke._normalize(outline) if outline is not None else None
        self.bars_offset = bars_offset
        self.bars_width = bars_width
