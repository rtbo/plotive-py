from typing import Literal

from .color import Color
from .geom import Padding
from .style import Fill, Stroke

type FigLegendPos = Literal[
    "auto",
    "top",
    "right",
    "bottom",
    "left",
]

type PlotLegendPos = Literal[
    "auto",
    "out-top",
    "out-bottom",
    "out-left",
    "out-right",
    "in-top-left",
    "in-top-right",
    "in-bottom-left",
    "in-bottom-right",
    "in-top",
    "in-bottom",
    "in-left",
    "in-right",
]

class Legend[PosType: FigLegendPos | PlotLegendPos]:
    """Legend display settings."""

    def __init__(
        self,
        pos: PosType = "auto",
        *,
        fill: Fill | Color | None = Fill("legend-fill", opacity=0.5),
        border: Stroke | str | None = "foreground",
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
        fill: Fill | Color | None, default=Fill("legend-fill", opacity=0.5)
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
        self.fill = Fill._normalize(fill) if fill is not None else None
        self.border = Stroke._normalize(border, default_width=1.0) if border is not None else None
        self.columns = columns
        self.margin = margin
        self.padding = padding
        self.spacing = spacing

type FigLegend = Legend[FigLegendPos]
type PlotLegend = Legend[PlotLegendPos]
