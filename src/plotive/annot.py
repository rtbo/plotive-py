"""Annotation objects that can be overlaid on plots."""

from abc import ABC
from typing import TYPE_CHECKING, Literal

from .color import Color

from .text import Text

from . import style
from .mapping import PvMapping
from .style import Pattern, Stroke

if TYPE_CHECKING:
    from .style import Fill

type ZPos = Literal["above-series", "below-series"]

type CoordSys = Literal["data", "plot"]
type Coord = float | tuple[float, CoordSys]
"""Coordinate can be a number (in data coordinates) or a tuple of [number, CoordSys] where the number is in the specified coordinate system.
If the coordinate system is not specified, it defaults to "data" coordinates.
In plot coordinates, the number is in points relative to the top-left corner of the plot area.
Negative numbers are allowed and will be interpreted as offsets from the right or bottom edges of the plot area.
"""


class Annotation(ABC, PvMapping):
    """Base class for plot annotations."""

    def __init__(
        self,
        x_axis: str | None = None,
        y_axis: str | None = None,
        z_pos: ZPos = "above-series",
    ):
        """Initialize common annotation settings.

        Parameters
        ----------
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        z_pos : str, default="above-series"
            Rendering layer relative to series.
        """
        self.type = self.__class__.__name__.lower()
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_pos = z_pos


class Line(Annotation):
    """Line annotation in horizontal, vertical, or geometric form."""

    def __init__(
        self,
        *,
        horizontal: Coord | None = None,
        vertical: Coord | None = None,
        slope: None | tuple[tuple[Coord, Coord], float] = None,
        two_points: None | tuple[tuple[Coord, Coord], tuple[Coord, Coord]] = None,
        stroke: None | Stroke = None,
        pattern: None | Pattern = None,
        x_axis: str | None = None,
        y_axis: str | None = None,
        z_pos: ZPos = "below-series",
    ):
        """Initialize a line annotation.

        Parameters
        ----------
        horizontal : Coord | None, default=None
            Horizontal line position ``y = constant``.
        vertical : Coord | None, default=None
            Vertical line position ``x = constant``.
        slope : tuple[tuple[Coord, Coord], float] | None, default=None
            Point-slope representation ``((x0, y0), m)``.
        two_points : tuple[tuple[Coord, Coord], tuple[Coord, Coord]] | None, default=None
            Two-point representation of the line.
        stroke : Stroke | None, default=None
            Stroke style.
        pattern : str | list[float] | None, default=None
            Optional dash pattern shortcut.
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        z_pos : ZPos, default="below-series"
            Rendering layer relative to series.

        Raises
        ------
        ValueError
            If none or more than one line definition is provided.
        """
        super().__init__(x_axis=x_axis, y_axis=y_axis, z_pos=z_pos)
        if sum(x is not None for x in [horizontal, vertical, slope, two_points]) != 1:
            raise ValueError(
                "Exactly one of 'horizontal', 'vertical', 'slope', or 'two_points' must be provided."
            )
        self.horizontal = horizontal
        self.vertical = vertical
        self.slope = slope
        self.two_points = two_points

        if isinstance(stroke, str):
            stroke = Stroke(color=stroke)
        if pattern is not None and stroke is not None:
            print(
                "Warning: both 'pattern' and 'stroke' are provided, the pattern of the stroke will be discarded."
            )
            stroke.pattern = pattern
        elif pattern is not None:
            stroke = Stroke(color="foreground", pattern=pattern)
        self.stroke = stroke


class Arrow(Annotation):
    """Arrow annotation defined by origin and delta."""

    def __init__(
        self,
        *,
        xy: tuple[Coord, Coord],
        dxy: tuple[float, float],
        stroke: None | Stroke = None,
        head_size: float = 10.0,
        x_axis: str | None = None,
        y_axis: str | None = None,
        z_pos: ZPos = "above-series",
    ):
        """Initialize an arrow annotation.

        Parameters
        ----------
        xy : tuple[Coord, Coord]
            Arrow origin.
        dxy : tuple[float, float]
            Arrow displacement vector.
        stroke : Stroke | None, default=None
            Stroke style.
        head_size : float, default=10.0
            Arrow head size in pixels.
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        z_pos : ZPos, default="above-series"
            Rendering layer relative to series.
        """
        super().__init__(x_axis=x_axis, y_axis=y_axis, z_pos=z_pos)
        self.xy = xy
        self.dxy = dxy
        if isinstance(stroke, str):
            stroke = Stroke(color=stroke)
        self.stroke = stroke
        self.head_size = head_size


class Marker(Annotation):
    """Marker annotation placed in data space."""

    def __init__(
        self,
        xy: tuple[float, float],
        *,
        marker: style.Marker = style.Marker(),
        x_axis: str | None = None,
        y_axis: str | None = None,
        z_pos: ZPos = "above-series",
    ):
        """Initialize a marker annotation.

        Parameters
        ----------
        xy : tuple[float, float]
            Marker position.
        marker : style.Marker, default=style.Marker()
            Marker style.
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        z_pos : ZPos, default="above-series"
            Rendering layer relative to series.
        """
        super().__init__(x_axis=x_axis, y_axis=y_axis, z_pos=z_pos)
        self.xy = xy
        self.marker = marker


type Anchor = Literal[
    "top-left",
    "top-center",
    "top-right",
    "center-left",
    "center",
    "center-right",
    "bottom-left",
    "bottom-center",
    "bottom-right",
]


class Label(Annotation):
    """Text label annotation placed in data space."""

    def __init__(
        self,
        xy: tuple[Coord, Coord],
        text: Text,
        *,
        anchor: Anchor = "top-left",
        frame: None | tuple[Fill | None, Stroke | Color | None] = None,
        angle: float = 0.0,
        x_axis: str | None = None,
        y_axis: str | None = None,
        z_pos: ZPos = "above-series",
    ):
        """Initialize a text label annotation.

        Parameters
        ----------
        xy : tuple[Coord, Coord]
            Label anchor position.
        text : str
            Label content.
        anchor : str, default="top-left"
            Text anchor relative to ``xy``.
        color : Color | None, default=None
            Text color.
        frame : tuple[Fill | None, Stroke | str | None] | None, default=None
            Optional frame as ``(fill, stroke)``.
        angle : float, default=0.0
            Label rotation angle in degrees.
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        z_pos : ZPos, default="above-series"
            Rendering layer relative to series.
        """
        super().__init__(x_axis=x_axis, y_axis=y_axis, z_pos=z_pos)
        self.xy = xy
        self.text = text
        self.anchor = anchor
        if frame is not None:
            fill, stroke = frame
            if isinstance(stroke, str):
                stroke = Stroke(color=stroke)
            self.frame = (fill, stroke)
        self.angle = angle
