"""Global styling primitives for figures and series."""

from .color import Color

type Fill[C=Color] = C
"""Type alias for fill colors."""


class Stroke[C=Color]:
    """Line stroke style.

    Parameters
    ----------
    color : Color or ThemeColor or SeriesColor (depending on context)
        Stroke color.
    width : float, default=1.0
        Stroke width in pixels.
    pattern : list[float] | str | None, default=None
        Dash pattern specification.
    opacity : float, default=1.0
        Stroke opacity in the ``[0, 1]`` interval.
    """

    def __init__(
        self,
        *,
        color: C,
        width: float = 1.0,
        pattern: None | list[float] | str = None,
        opacity: float = 1.0,
    ):
        """Initialize a stroke style."""
        self.color = color
        self.width = width
        self.pattern = pattern
        self.opacity = opacity

class Marker[C]:
    """Marker style for scatter series.

    Parameters
    ----------
    shape : str
        Marker shape. One of "circle", "square", "cross", "plus", "triangle-up", "triangle-down".
    size : float, default=10.0
        Marker size in pixels.
    fill : Fill[C] | None, default=None
        Marker fill color.
    stroke : Stroke[C] | None, default=None
        Marker stroke style.
    """

    def __init__(
        self,
        *,
        shape: str = "circle",
        size: float = 10.0,
        fill: None | Fill[C] = "auto",
        stroke: None | Stroke[C] = None,
    ):
        """Initialize a marker style."""
        self.shape = shape
        self.size = size
        self.fill = fill
        self.stroke = stroke

class ThemePalette:
    """Theme palette for structural chart colors.

    Parameters
    ----------
    background : Color | None, default=None
        Figure background color.
    foreground : Color | None, default=None
        Main foreground color.
    grid : Color | None, default=None
        Grid line color.
    axis : Color | None, default=None
        Axis line and tick color.
    text : Color | None, default=None
        Text color.
    """

    def __init__(
        self,
        *,
        background: None | Color = None,
        foreground: None | Color = None,
        grid: None | Color = None,
        axis: None | Color = None,
        text: None | Color = None,
    ):
        """Initialize a theme palette."""
        self.background = background
        self.foreground = foreground
        self.grid = grid
        self.axis = axis
        self.text = text


type Theme = ThemePalette | str
"""Explicit theme object or predefined theme name."""

type SeriesPalette = list[Color] | str
"""Explicit series palette or predefined palette name."""


class Style:
    """Top-level style configuration for figure rendering.

    Parameters
    ----------
    theme : Theme | None, default=None
        Figure theme configuration.
    palette : SeriesPalette | None, default=None
        Color palette used for data series.
    """

    def __init__(
        self,
        *,
        theme: None | Theme = None,
        palette: None | SeriesPalette = None,
    ):
        """Initialize global style settings."""
        self.theme = theme
        self.palette = palette
