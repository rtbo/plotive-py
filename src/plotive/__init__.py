"""High-level public API for building and exporting Plotive figures."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from plotive.style import ThemeFill

if TYPE_CHECKING:
    from .style import Stroke, Fill, Style

from .annot import Annotation
from .axis import *
from .series import Series

type Size = tuple[float, float]
"""Figure size in pixels as ``(width, height)``."""

type Padding = float | tuple[float, float] | tuple[float, float, float, float]
"""Padding as scalar, ``(vertical, horizontal)``, or ``(top, right, bottom, left)``."""

type DataSource = object
"""
User-provided data source resolved at render time.
Accepted objects are dictionaries of numpy arrays, dictionaries of lists, pandas DataFrames
"""


class Legend:
    """Legend display settings."""

    def __init__(
        self,
        pos: str,
        *,
        fill: ThemeFill | ThemeColor | None = ThemeFill("legend-fill", opacity=0.5),
        border: Stroke | str = "foreground",
        columns: None | int = None,
        margin: float = 12,
        padding: Padding = 8,
        spacing: float | tuple[float, float] = (16, 10),
    ):
        """Initialize a legend.
        Parameters
        ----------
        pos : str, default="bottom"
            Legend position as a string. Accepted values depends whether the legend is attached to a figure or a plot.
            Accepted figure legend positions are "top", "bottom", "left" and "right".
            Accepted plot legend positions are "out-top", "out-bottom", "out-left", "out-right",
            "in-top-left", "in-top-right", "in-bottom-left" and "in-bottom-right",
            "in-top", "in-bottom", "in-left" and "in-right".
            "auto" is also accepted for default position at the bottom.
        fill: ThemeFill | ThemeColor | None, default=ThemeFill("legend-fill", opacity=0.5)
            Legend background fill.
        border : Stroke | str, default="foreground"
            Stroke style of the legend border.
        columns : int | None, default=None
            Number of columns in the legend.
            If None, the number of columns is determined automatically based on the position and number of entries.
        margin : float, default=12
            Margin between the legend and the figure/plot edges in pixels.
        padding : Padding, default=8
            Padding inside the legend box.
        spacing : float or tuple[float, float], default=(16, 10)
            Spacing between legend entries (horizontal, vertical).
        """
        self.pos = pos
        self.fill = fill and ThemeFill._normalize(fill)
        self.border = border
        self.columns = columns
        self.margin = margin
        self.padding = padding
        self.spacing = spacing


class ColorBar:
    def __init__(
        self,
        pos: str = "right",
        *,
        width: float = 20.0,
        title: str | None = None,
        border: ThemeStroke | ThemeColor | None = "foreground",
        ticks: None | axis.TicksLocator | list[float] | list[int] = None,
        margin: float = 12.0,
    ):
        if pos == "auto":
            pos = "right"
        self.pos = pos
        self.width = width
        self.title = title
        self.border = ThemeStroke._normalize(border) if border is not None else None
        self.ticks = axis.TicksLocator._normalize(ticks) if ticks is not None else None
        self.margin = margin

    @staticmethod
    def _normalize(input: str | ColorBar) -> "ColorBar":
        if isinstance(input, ColorBar):
            return input
        elif isinstance(input, str):
            return ColorBar(pos=input)
        else:
            raise ValueError(f"Invalid colorbar config: {input!r}")

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
"""Predefined ticks that fits well the stellar colormap."""

class Plot:
    """Single subplot definition with series, axes, and annotations."""

    def __init__(
        self,
        series: list[Series] | Series,
        *,
        x_axis: None | Axis = None,
        y_axis: None | Axis = None,
        x_axes: None | list[Axis] = None,
        y_axes: None | list[Axis] = None,
        subplot: None | tuple[int, int] = None,
        title: None | str = None,
        legend: None | Legend | str = None,
        colorbar: None | ColorBar | str = None,
        annotations: list[Annotation] = [],
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
        title : str | None, default=None
            Subplot title.
        legend : Legend | str | None, default=None
            Subplot legend config or shortcut position.
        colorbar : ColorBar | None | str, default=None
            Subplot colorbar config.
        annotations : list[Annotation], default=[]
            Annotation objects attached to this plot.

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
            if legend == "auto":
                legend = "out-bottom"
            self.legend = Legend(pos=legend)
        else:
            self.legend = legend

        self.colorbar = ColorBar._normalize(colorbar) if colorbar is not None else None

        self.annotations = annotations

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

        # Sanity check
        for ax in self.x_axes:
            if hasattr(ax, "_side") and (ax._side == "left" or ax._side == "right"):
                raise ValueError("X-axis cannot be on the left or right side.")
        for ax in self.y_axes:
            if hasattr(ax, "_side") and (ax._side == "top" or ax._side == "bottom"):
                raise ValueError("Y-axis cannot be on the top or bottom side.")


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


class Figure:
    """Top-level container for one or more plots."""

    def __init__(
        self,
        /,
        *,
        title: None | str = None,
        size: None | Size = (800, 600),
        padding: None | Padding = 20.0,
        fill: None | ThemeFill | ThemeColor = "background",
        legend: None | Legend | str = None,
        plot: None | Plot = None,
        plots: None | list[Plot] = None,
    ):
        """Initialize a figure.

        Parameters
        ----------
        title : str | None, default=None
            Figure title.
        size : Size | None, default=(800, 600)
            Output size in pixels.
        padding : Padding | None, default=20.0
            Figure inner padding.
        fill : ThemeFill | ThemeColor | None, default="background"
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
        self.fill = fill and ThemeFill._normalize(fill)
        if isinstance(legend, str):
            self.legend = Legend(pos=legend)
        else:
            self.legend = legend

    def render_pxl(
        self, *, data_source: None | DataSource = None, style: None | Style | str = None
    ) -> PxlArray:
        """Render the figure as an array of pixels

        Parameters
        ----------
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | str | None, default=None
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
        style: None | Style | str = None,
    ):
        """Export the figure as PNG.

        Parameters
        ----------
        path : str
            Output file path.
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | str | None, default=None
            Rendering style object or style name.
        """
        from ._rs import save_png as rs_save_png

        rs_save_png(self, path, data_source, style)

    def save_svg(
        self,
        path: str,
        *,
        data_source: None | DataSource = None,
        style: None | Style | str = None,
    ):
        """Export the figure as SVG.

        Parameters
        ----------
        path : str
            Output file path.
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | str | None, default=None
            Rendering style object or style name.
        """
        from ._rs import save_svg as rs_save_svg

        rs_save_svg(self, path, data_source, style)

    def show(
        self, *, data_source: None | DataSource = None, style: None | Style | str = None
    ):
        """Display the figure in an interactive viewer.

        Parameters
        ----------
        data_source : DataSource | None, default=None
            Runtime data source.
        style : Style | str | None, default=None
            Rendering style object or style name.
        """
        from ._rs import show as rs_show

        rs_show(self, data_source, style)
