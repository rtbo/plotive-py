"""Annotation objects that can be overlaid on plots."""

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .style import Fill
    from .color import Color

from .style import Stroke


class Annotation(ABC):
    """Base class for plot annotations."""

    def __init__(
        self, x_axis: str | None = None, y_axis: str | None = None, zpos: str = "above-series"
    ):
        """Initialize common annotation settings.

        Parameters
        ----------
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        zpos : str, default="above-series"
            Rendering layer relative to series.
        """
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.zpos = zpos

    def _get_type(self) -> str:
        """Return the concrete annotation type name."""
        return self.__class__.__name__


class Line(Annotation):
    """Line annotation in horizontal, vertical, or geometric form."""

    def __init__(
        self,
        *,
        horizontal: float | None = None,
        vertical: float | None = None,
        slope: None | tuple[tuple[float, float], float] = None,
        two_points: None | tuple[tuple[float, float], tuple[float, float]] = None,
        stroke: None | Stroke = None,
        pattern: None | str | list[float] = None,
        x_axis: str | None = None,
        y_axis: str | None = None,
        zpos: str = "below-series",
    ):
        """Initialize a line annotation.

        Parameters
        ----------
        horizontal : float | None, default=None
            Horizontal line position ``y = constant``.
        vertical : float | None, default=None
            Vertical line position ``x = constant``.
        slope : tuple[tuple[float, float], float] | None, default=None
            Point-slope representation ``((x0, y0), m)``.
        two_points : tuple[tuple[float, float], tuple[float, float]] | None, default=None
            Two-point representation of the line.
        stroke : Stroke | None, default=None
            Stroke style.
        pattern : str | list[float] | None, default=None
            Optional dash pattern shortcut.
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        zpos : str, default="below-series"
            Rendering layer relative to series.

        Raises
        ------
        ValueError
            If none or more than one line definition is provided.
        """
        super().__init__(x_axis=x_axis, y_axis=y_axis, zpos=zpos)
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
        xy: tuple[float, float],
        delta: tuple[float, float],
        stroke: None | Stroke = None,
        head_size: float = 10.0,
        x_axis: str | None = None,
        y_axis: str | None = None,
        zpos: str = "above-series",
    ):
        """Initialize an arrow annotation.

        Parameters
        ----------
        xy : tuple[float, float]
            Arrow origin.
        delta : tuple[float, float]
            Arrow displacement vector.
        stroke : Stroke | None, default=None
            Stroke style.
        head_size : float, default=10.0
            Arrow head size in pixels.
        x_axis : str | None, default=None
            Target x-axis identifier.
        y_axis : str | None, default=None
            Target y-axis identifier.
        zpos : str, default="above-series"
            Rendering layer relative to series.
        """
        super().__init__(x_axis=x_axis, y_axis=y_axis, zpos=zpos)
        self.x, self.y = xy
        self.dx, self.dy = delta
        if isinstance(stroke, str):
            stroke = Stroke(color=stroke)
        self.stroke = stroke
        self.head_size = head_size


class Label(Annotation):
    """Text label annotation placed in data space."""

    def __init__(
        self,
        xy: tuple[float, float],
        text: str,
        *,
        anchor: str = "top-left",
        color: None | Color = None,
        frame: None | tuple[Fill | None, Stroke | str | None] = None,
        angle: float = 0.0,
        x_axis: str | None = None,
        y_axis: str | None = None,
        zpos: str = "above-series",
    ):
        """Initialize a text label annotation.

        Parameters
        ----------
        xy : tuple[float, float]
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
        zpos : str, default="above-series"
            Rendering layer relative to series.
        """
        super().__init__(x_axis=x_axis, y_axis=y_axis, zpos=zpos)
        self.x, self.y = xy
        self.text = text
        self.anchor = anchor
        self.color = color
        if frame is not None:
            fill, stroke = frame
            if isinstance(stroke, str):
                stroke = Stroke(color=stroke)
            self.frame = (fill, stroke)
        self.angle = angle
