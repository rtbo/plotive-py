"""High-level public API for building and exporting Plotive figures."""

from collections.abc import Mapping

from . import mapping
from .style import *
from .annot import Annotation
from .axis import *
from .color import Color
from .colorbar import ColorBar, ColorBarPos
from .geom import Padding, Size
from .legend import FigLegend, FigLegendPos, Legend, PlotLegend, PlotLegendPos
from .series import Series
from .text import Text

type DataSource = object
"""
User-provided data source resolved at render time.
Accepted objects are dictionaries of numpy arrays, dictionaries of lists, pandas DataFrames
"""


STELLAR_TICKS = [
    1000.0,
    2000.0,
    3000.0,
    4000.0,
    5000.0,
    6500.0,
    8000.0,
    10000.0,
    12500.0,
    15000.0,
]
"""Predefined ticks that fits well with the stellar colormap."""

type PlotBorderType = Literal["box", "axis", "arrow"]

class PlotBorder(ABC, mapping.PvMapping):
    """Border configuration for a plot."""
    def __init__(
        self,
        type: PlotBorderType,
    ):
        self.type = type

class BoxPlotBorder(PlotBorder):
    """Box border configuration for a plot."""
    def __init__(self, stroke: None | Stroke | Color = None):
        super().__init__(type="box")
        self.stroke = stroke

class AxisPlotBorder(PlotBorder):
    """Axis border configuration for a plot."""
    def __init__(self, stroke: None | Stroke | Color = None):
        super().__init__(type="axis")
        self.stroke = stroke

class ArrowPlotBorder(PlotBorder):
    """Arrow border configuration for a plot."""
    def __init__(self, stroke: None | Stroke | Color = None):
        super().__init__(type="arrow")
        self.stroke = stroke

class Plot(mapping.PvMapping):
    """Single subplot definition with series, axes, and annotations."""

    def __init__(
        self,
        series: list[Series] | Series,
        *,
        title: None | Text = None,
        x_axis: None | Axis = None,
        y_axis: None | Axis = None,
        x_axes: None | list[Axis] = None,
        y_axes: None | list[Axis] = None,
        subplot: None | tuple[int, int] = None,
        fill: None | ThemeFill | ThemeColor = None,
        legend: None | PlotLegend | PlotLegendPos = None,
        colorbar: None | ColorBar | ColorBarPos = None,
        annotations: list[Annotation] | None = None,
        border: None | PlotBorderType | PlotBorder | ThemeColor = "box",
    ):
        """Initialize a plot.
        By default, a plot has a single x and y axis, without any ticks, labels or grid.

        Parameters
        ----------
        series : list[Series]
            Data series to render.
        x_axis : Axis | None, default=None
            Convenience single x-axis.
        y_axis : Axis | None, default=None
            Convenience single y-axis.
        x_axes : list[Axis] | None, default=None
            Explicit list of x-axes.
        y_axes : list[Axis] | None, default=None
            Explicit list of y-axes.
        subplot : tuple[int, int] | None, default=None
            Grid position of the subplot.
            Only relevant when multiple plots are defined in the same figure.
        title : Text | None, default=None
            Subplot title.
        fill : Fill | Color | None, default=None
            Background fill for the plot area.
        legend : Legend | PlotLegendPos | None, default=None
            Subplot legend config or shortcut position.
        colorbar : ColorBar | None | ColorBarPos, default=None
            Subplot colorbar config.
        annotations : list[Annotation], default=[]
            Annotation objects attached to this plot.
        border : PlotBorderType | PlotBorder | ThemeColor | None, default=None
            Border configuration for the plot.

        Raises
        ------
        ValueError
            If both single-axis and multi-axis variants are provided.
        """
        self.title = title
        self.subplot = subplot

        if isinstance(series, list):
            self.series = series
        else:
            self.series = [series]

        if isinstance(legend, str):
            legend = Legend(pos=legend)
        self.legend = legend

        self.fill = fill

        self.colorbar = colorbar

        self.annotations = annotations if annotations is not None else []

        if x_axis is not None and x_axes is not None:
            raise ValueError("Cannot provide both 'x_axis' and 'x_axes'.")
        if y_axis is not None and y_axes is not None:
            raise ValueError("Cannot provide both 'y_axis' and 'y_axes'.")

        self.x_axes = (
            x_axes
            if x_axes is not None
            else ([x_axis] if x_axis is not None else [Axis()])
        )
        self.y_axes = (
            y_axes
            if y_axes is not None
            else ([y_axis] if y_axis is not None else [Axis()])
        )
        self.border = border


class PxlArray:
    """Array of pixels returned by the renderer.

    The data contains raw RGBA premultiplied pixel data, with 8 bits per channel.
    """

    def __init__(self, data: bytearray, width: int, height: int):
        self.data = data
        self.width = width
        self.height = height

    def depremultiply(self) -> bytes:
        """Return non-premultiplied pixel data."""
        for i in range(0, len(self.data), 4):
            r, g, b, a = self.data[i : i + 4]
            if a > 0 and a < 255:
                r = int(r * 255 / a)
                g = int(g * 255 / a)
                b = int(b * 255 / a)
                self.data[i : i + 4] = bytes([r, g, b, a])
        return self.data


class Figure(mapping.PvMapping):
    """Top-level container for one or more plots."""

    def __init__(
        self,
        /,
        *,
        size: None | Size = (800, 600),
        title: None | Text = None,
        plot: None | Plot = None,
        plots: None | list[Plot] = None,
        padding: None | Padding = None,
        fill: None | ThemeFill | ThemeColor = "background",
        legend: None | FigLegend | FigLegendPos = None,
        space: None | float = None,
    ):
        """Initialize a figure.

        Parameters
        ----------
        title : str | None, default=None
            Figure title.
        size : Size | None, default=(800, 600)
            Output size in pixels.
        padding : Padding | None, default=None
            Figure inner padding.
        fill : Fill | Color | None, default="background"
            Figure background fill.
        legend : Legend | str | None, default=None
            Figure-level legend config or shortcut position.
        plot : Plot | None, default=None
            Convenience single plot.
        plots : list[Plot] | None, default=None
            Explicit list of plots.

        Raises
        ------
        ValueError
            If neither ``plot`` nor ``plots`` is provided.
        """
        if plot is not None:
            self.plots = [plot]
        elif plots is not None:
            self.plots = plots
        else:
            raise ValueError("Either 'plot' or 'plots' must be provided.")

        self.title = title
        self.size = size
        self.padding = padding
        self.fill = fill
        self.legend = legend
        self.space = space

    def render_pxl(
        self, *, data_source: None | DataSource = None, style: None | Style | BuiltinStyle = None
    ) -> PxlArray:
        """Render the figure as an array of pixels

        Parameters
        ----------
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | BuiltinStyle | None, default=None
            Rendering style object or style name.
        """
        from ._rs import render_pxl as rs_render_pxl

        data, width, height = rs_render_pxl(self, data_source, style)
        return PxlArray(data, width, height)

    def save_png(
        self,
        path: str,
        *,
        data_source: None | DataSource = None,
        style: None | Style | BuiltinStyle = None,
    ):
        """Export the figure as PNG.

        Parameters
        ----------
        path : str
            Output file path.
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | BuiltinStyle | None, default=None
            Rendering style object or style name.
        """
        from ._rs import save_png as rs_save_png

        rs_save_png(self, path, data_source, style)

    def save_svg(
        self,
        path: str,
        *,
        data_source: None | DataSource = None,
        style: None | Style | BuiltinStyle = None,
    ):
        """Export the figure as SVG.

        Parameters
        ----------
        path : str
            Output file path.
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | BuiltinStyle | None, default=None
            Rendering style object or style name.
        """
        from ._rs import save_svg as rs_save_svg

        rs_save_svg(self, path, data_source, style)

    def show(
        self, *, data_source: None | DataSource = None, style: None | Style | BuiltinStyle = None
    ):
        """Display the figure in an interactive viewer.

        Parameters
        ----------
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | BuiltinStyle | None, default=None
            Rendering style object or style name.
        """
        from ._rs import show as rs_show

        rs_show(self, data_source, style)
