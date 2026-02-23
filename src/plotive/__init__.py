from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .style import Stroke, Fill, Style

from .annot import Annotation
from .axis import *
from .series import Series

type Size = tuple[float, float]
type Padding = float | tuple[float, float] | tuple[float, float, float, float]

type DataSource = object


@dataclass(kw_only=True)
class Legend:
    pos: str = "bottom"
    border: Stroke | str = "foreground"
    columns: None | int = None
    margin: float = 12
    padding: Padding = 8
    spacing: float | tuple[float, float] = (16, 10)


class Plot:
    def __init__(
        self,
        *,
        series: list[Series],
        x_axis: None | Axis = None,
        y_axis: None | Axis = None,
        x_axes: None | list[Axis] = None,
        y_axes: None | list[Axis] = None,
        subplot: None | tuple[int, int] = None,
        title: None | str = None,
        legend: None | Legend | str = None,
        annotations: list[Annotation] = [],
    ):
        self.title = title
        self.subplot = subplot
        self.series = series
        if isinstance(legend, str):
            self.legend = Legend(pos=legend)
        else:
            self.legend = legend
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


class Figure:
    def __init__(
        self,
        /,
        *,
        title: None | str = None,
        size: None | Size = (800, 600),
        padding: None | Padding = 20.0,
        fill: None | Fill = "background",
        legend: None | Legend | str = None,
        plot: None | Plot = None,
        plots: None | list[Plot] = None,
    ):
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
        if isinstance(legend, str):
            self.legend = Legend(pos=legend)
        else:
            self.legend = legend

    def save_png(
        self,
        path: str,
        *,
        data_source: None | DataSource = None,
        style: None | Style | str = None,
    ):
        from ._rs import save_png as rs_save_png

        rs_save_png(self, path, data_source, style)

    def save_svg(
        self,
        path: str,
        *,
        data_source: None | DataSource = None,
        style: None | Style | str = None,
    ):
        from ._rs import save_png as rs_save_svg

        rs_save_svg(self, path, data_source, style)

    def show(
        self, *, data_source: None | DataSource = None, style: None | Style | str = None
    ):
        from ._rs import show as rs_show

        rs_show(self, data_source, style)
