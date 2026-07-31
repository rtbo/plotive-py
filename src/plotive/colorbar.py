from typing import Literal

from .mapping import PvMapping

from . import axis
from .color import Color
from .style import Stroke
from .text import Text

type ColorBarPos = Literal["auto", "top", "right", "bottom", "left"]


class ColorBar(PvMapping):
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
        self.border = border
        self.ticks = ticks
        self.margin = margin
