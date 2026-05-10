"""Data series objects that can be rendered in a plot."""

from abc import ABC
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from datetime import datetime
    from .style import Fill, Color, SeriesColor

from .style import SeriesFill, SeriesMarker, SeriesStroke

type DataCol = str | list[float] | list[str] | list[datetime] | np.ndarray
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
        line: SeriesStroke | SeriesColor = SeriesStroke(),
        interpolation: None | str = None,
        marker: SeriesMarker | None = None,
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
        line : SeriesStroke | SeriesColor | None, default=None
            Line stroke style or color.
        interpolation : str | None, default=None
            Interpolation mode for rendering.
        marker : SeriesMarker | None, default=None
            Marker style. If None, no marker will be rendered.    let ?;
        """
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = x
        self.y = y
        self.line = SeriesStroke._normalize(line)
        self.interpolation = interpolation
        self.marker = marker

class Scatter(Series):
    """Scatter series defined by x/y coordinates."""

    def __init__(
        self,
        x: DataCol,
        y: DataCol,
        *,
        name: None | str = None,
        sizes: None | DataCol = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
        marker: SeriesMarker = SeriesMarker(),
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
        name : str | None, default=None
            Legend/display name of the series.
        x_axis : AxisRef | None, default=None
            Target x-axis reference.
        y_axis : AxisRef | None, default=None
            Target y-axis reference.
        marker : SeriesMarker, default=SeriesMarker()
            Marker style. If None, the marker will be automatically assigned based on the series palette.
        """
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = x
        self.y = y
        self.sizes = sizes
        self.marker = marker

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
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
        fill: SeriesFill | SeriesColor = SeriesFill(),
        y1_line: SeriesStroke | SeriesColor | None = None,
        y2_line: SeriesStroke | SeriesColor | None = None,
        y1_interpolation: None | str = None,
        y2_interpolation: None | str = None,
        interpolation: None | str = None,
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
        name : str | None, default=None
            Legend/display name of the series.
        x_axis : AxisRef | None, default=None
            Target x-axis reference.
        y_axis : AxisRef | None, default=None
            Target y-axis reference.
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
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
        fill: None | SeriesFill | SeriesColor  = "auto",
        outline: None | SeriesStroke | SeriesColor = None,
        bins: int = 10,
        density: bool = False,
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
        name: None | str = None,
        x_axis: None | AxisRef = None,
        y_axis: None | AxisRef = None,
        fill: None | SeriesFill | SeriesColor  = "auto",
        outline: None | SeriesStroke | SeriesColor = None,
        bars_offset = 0.3,
        bars_width = 0.4,
    ):
        super().__init__(name=name, x_axis=x_axis, y_axis=y_axis)
        self.x = x
        self.y = y
        self.fill = SeriesFill._normalize(fill) if fill is not None else None
        self.outline = SeriesStroke._normalize(outline) if outline is not None else None
        self.bars_offset = bars_offset
        self.bars_width = bars_width
