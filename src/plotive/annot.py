from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .style import Fill
    from .color import Color

from .style import Stroke


class Annotation(ABC):
    def __init__(
        self, x_axis: str | None = None, y_axis: str | None = None, zpos: str = "above-series"
    ):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.zpos = zpos

    def _get_type(self) -> str:
        return self.__class__.__name__


class Line(Annotation):
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
        super().__init__(x_axis=x_axis, y_axis=y_axis, zpos=zpos)
        self.x, self.y = xy
        self.dx, self.dy = delta
        if isinstance(stroke, str):
            stroke = Stroke(color=stroke)
        self.stroke = stroke
        self.head_size = head_size


class Label(Annotation):
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
