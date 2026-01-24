from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .color import Color

type Fill = Color

@dataclass(kw_only=True)
class Stroke:
    color: Color
    width: float = 1.0
    pattern: None | list[float] = None
    opacity: float = 1.0

class ThemePalette:
    def __init__(
        self,
        *,
        background: None | Color = None,
        foreground: None | Color = None,
        grid: None | Color = None,
        axis: None | Color = None,
        text: None | Color = None,
    ):
        self.background = background
        self.foreground = foreground
        self.grid = grid
        self.axis = axis
        self.text = text


type Theme = ThemePalette | str

type SeriesPalette = list[Color] | str

class Style:
    def __init__(
        self,
        *,
        theme: None | Theme = None,
        palette: None | SeriesPalette = None,
    ):
        self.theme = theme
        self.palette = palette
