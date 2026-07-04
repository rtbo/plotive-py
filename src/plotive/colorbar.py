

from typing import Literal

from . import axis
from .color import Color
from .style import Stroke
from .text import Text

type ColorBarPos = Literal["auto", "top", "right", "bottom", "left"]

class ColorBar:
    def __init__(
        self,
        pos: ColorBarPos = "right",
        *,
        width: float = 20.0,
        title: Text | None = None,
        border: Stroke | Color | None = "foreground",
        ticks: None | axis.TicksLocator | list[float] | list[int] = None,
        margin: float = 12.0,
    ):
        if pos == "auto":
            pos = "right"
        self.pos = pos
        self.width = width
        self.title = title
        self.border = (
            Stroke._normalize(border, default_width=1.0) if border is not None else None
        )
        self.ticks = axis.TicksLocator._normalize(ticks) if ticks is not None else None
        self.margin = margin

    @staticmethod
    def _normalize(input: ColorBarPos | ColorBar) -> "ColorBar":
        if isinstance(input, ColorBar):
            return input
        elif isinstance(input, str):
            return ColorBar(pos=input)
        else:
            raise ValueError(f"Invalid colorbar config: {input!r}")
